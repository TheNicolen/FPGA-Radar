#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RadarLink HMI - Nexys Video -> Ethernet UDP -> Jetson Nano.

Compatible con Python >= 3.6 y PyQt5 (sin pyqtgraph).
El protocolo actual SOLO envia detecciones; RAD2 transporta detecciones y RADQ transporta muestras I/Q sintéticas.
"""
import argparse
import csv
import math
import socket
import struct
import sys
import time
from collections import deque
from datetime import datetime

from PyQt5.QtCore import Qt, QTimer, QSocketNotifier, QRectF, QPointF
from PyQt5.QtGui import QColor, QFont, QPainter, QPen, QBrush
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QTextEdit, QComboBox, QFileDialog, QSpinBox, QCheckBox,
    QSizePolicy, QMessageBox, QAbstractItemView
)

from radr_protocol import PORT, decode_packet
from radar_signal import decode_iq, spectrum
from radar_signal_views import PositionDisplay, SignalDisplay

HISTORY_LIMIT = 10000
ACTIVE_TIMEOUT_S = 3.0

COL_BG = QColor('#080f19')
COL_PANEL = QColor('#101e2c')
COL_GRID = QColor('#264258')
COL_GREEN = QColor('#42e99a')
COL_CYAN = QColor('#59d5f4')
COL_TEXT = QColor('#e1edf7')
COL_MUTED = QColor('#99afc1')


def panel(title):
    box = QFrame()
    box.setObjectName('panel')
    layout = QVBoxLayout(box)
    layout.setContentsMargins(12, 10, 12, 10)
    layout.setSpacing(8)
    header = QLabel(title)
    header.setObjectName('sectionTitle')
    layout.addWidget(header)
    return box, layout


def info_label(title, content):
    label = QLabel('{}  {}'.format(title, content))
    label.setObjectName('muted')
    return label


class RangeDisplay(QWidget):
    """Grafico 1D: X=distancia, Y=fila de ID. No representa azimut."""
    def __init__(self, parent=None):
        super(RangeDisplay, self).__init__(parent)
        self.targets = {}
        self.max_range = 120.0
        self.selected = None
        self.setMinimumSize(360, 280)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_data(self, targets, max_range, selected):
        self.targets = dict(targets)
        self.max_range = max(10.0, float(max_range))
        self.selected = selected
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), COL_BG)
        r = self.rect().adjusted(72, 25, -24, -54)
        if r.width() < 40 or r.height() < 60:
            return
        p.setFont(QFont('DejaVu Sans', 9))
        p.setPen(QPen(COL_GRID, 1))
        for i in range(6):
            x = r.left() + r.width() * i / 5.0
            p.drawLine(QPointF(x, r.top()), QPointF(x, r.bottom()))
            p.setPen(COL_MUTED)
            p.drawText(QRectF(x - 35, r.bottom() + 10, 70, 20), Qt.AlignHCenter,
                       '{:.0f}'.format(self.max_range * i / 5.0))
            p.setPen(QPen(COL_GRID, 1))
        p.setPen(COL_MUTED)
        p.drawText(QRectF(r.left(), r.bottom() + 33, r.width(), 18),
                   Qt.AlignCenter, 'Distancia radial (m)  |  SIN AZIMUT')

        ids = sorted(self.targets)
        if not ids:
            p.setPen(COL_MUTED)
            p.drawText(r, Qt.AlignCenter, 'Esperando detecciones UDP desde la Nexys Video...')
            return
        count = len(ids)
        for index, tid in enumerate(ids):
            item = self.targets[tid]
            y = r.top() + r.height() * (index + 0.5) / count
            p.setPen(QPen(COL_GRID, 1))
            p.drawLine(QPointF(r.left(), y), QPointF(r.right(), y))
            p.setPen(COL_MUTED)
            p.drawText(QRectF(3, y - 12, 64, 24), Qt.AlignVCenter, 'ID {}'.format(tid))
            d = item['range_m']
            if d > self.max_range or d < 0:
                continue
            x = r.left() + r.width() * d / self.max_range
            is_selected = tid == self.selected
            color = COL_GREEN if is_selected else COL_CYAN
            p.setPen(QPen(color, 2))
            p.setBrush(QBrush(color))
            p.drawEllipse(QPointF(x, y), 7 if is_selected else 5, 7 if is_selected else 5)
            p.setPen(COL_TEXT)
            label_x = min(x + 9, r.right() - 80)
            p.drawText(QRectF(label_x, y - 27, 95, 21), Qt.AlignLeft,
                       '{:.2f} m'.format(d))


class TrendDisplay(QWidget):
    """Distancia vs tiempo por ID; no es una onda RF ni un A-scope."""
    def __init__(self, parent=None):
        super(TrendDisplay, self).__init__(parent)
        self.samples = []
        self.selected = None
        self.max_range = 120.0
        self.setMinimumSize(360, 260)

    def set_data(self, samples, selected, max_range):
        self.samples = list(samples)
        self.selected = selected
        self.max_range = max_range
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), COL_BG)
        r = self.rect().adjusted(64, 26, -22, -52)
        if r.width() < 30 or r.height() < 40:
            return
        p.setPen(QPen(COL_GRID, 1))
        for i in range(5):
            yy = r.bottom() - r.height()*i/4.0
            p.drawLine(QPointF(r.left(), yy), QPointF(r.right(), yy))
            p.setPen(COL_MUTED)
            p.drawText(QRectF(2, yy-10, 54, 20), Qt.AlignRight,
                       '{:.0f}'.format(self.max_range*i/4.0))
            p.setPen(QPen(COL_GRID, 1))
        p.setPen(COL_MUTED)
        p.drawText(QRectF(r.left(), r.bottom()+26, r.width(), 20), Qt.AlignCenter,
                   'Tiempo reciente (60 s) - distancia del objetivo (m)')
        if self.selected is None:
            p.drawText(r, Qt.AlignCenter, 'Selecciona un ID en la tabla de objetivos')
            return
        points = [s for s in self.samples if s['id'] == self.selected]
        if len(points) < 2:
            p.drawText(r, Qt.AlignCenter, 'Esperando historial del ID {}'.format(self.selected))
            return
        now = time.monotonic()
        p.setPen(QPen(COL_CYAN, 2))
        prev = None
        for s in points:
            age = now-s['recv_mono']
            if not (0 <= age <= 60):
                prev = None
                continue
            x = r.right()-r.width()*age/60.0
            y = r.bottom()-r.height()*min(self.max_range, max(0, s['range_m']))/self.max_range
            curr = QPointF(x, y)
            if prev is not None:
                p.drawLine(prev, curr)
            prev = curr


class RadarWindow(QMainWindow):
    def __init__(self, port, max_range):
        super(RadarWindow, self).__init__()
        self.port = port
        self.max_range = max_range
        self.targets = {}
        self.scene_rows = {}
        self.history = deque(maxlen=HISTORY_LIMIT)
        self.events = deque(maxlen=500)
        self.rx = 0
        self.invalid = 0
        self.missing = 0
        self.duplicates = 0
        self.last_seq = None
        self.last_packet = None
        self.selected_id = None
        self.last_status = 'Esperando paquetes'
        self.sock = None
        self.notifier = None
        self.last_log_by_key = {}
        self._build_ui()
        self._open_socket()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_display)
        self.timer.start(100)  # 10 Hz: dibujo separado de recepcion
        self.log_event('HMI iniciado · detecciones y muestras I/Q de prueba')

    def _build_ui(self):
        self.setWindowTitle('RadarLink | Monitor radar - Nexys Video / Jetson Nano')
        self.resize(1330, 820)
        self.setMinimumSize(960, 610)
        root = QWidget()
        self.setCentralWidget(root)
        main = QVBoxLayout(root)
        main.setContentsMargins(12, 10, 12, 10)
        main.setSpacing(9)

        heading = QHBoxLayout()
        brand = QLabel('◉  RadarLink')
        brand.setObjectName('brand')
        heading.addWidget(brand)
        heading.addSpacing(18)
        heading.addWidget(QLabel('Nexys Video  /  Jetson Nano  ·  Monitor experimental'))
        heading.addStretch()
        self.status_label = QLabel('UDP: esperando')
        self.status_label.setObjectName('status')
        heading.addWidget(self.status_label)
        main.addLayout(heading)

        nav = QHBoxLayout()
        self.navbuttons = []
        self.pages = QStackedWidget()
        for i, name in enumerate(['Principal', 'Inicio', 'Onda', 'Espectro', 'Posición', 'Historial', 'Configuración']):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, page=i: self.show_page(page))
            nav.addWidget(btn)
            self.navbuttons.append(btn)
        main.addLayout(nav)
        main.addWidget(self.pages, 1)

        self._build_main_dashboard()
        self._build_home()
        self._build_wave()
        self._build_spectrum()
        self._build_position()
        self._build_history()
        self._build_settings()
        self.show_page(0)
        self.setStyleSheet('''
            QWidget { background: #0a1420; color: #e0edf6; font-family: "DejaVu Sans", "Ubuntu"; font-size: 12px; }
            QFrame#panel { background: #111f2e; border: 1px solid #345066; border-radius: 8px; }
            QLabel#brand { color: #66eca9; font-size: 23px; font-weight: bold; }
            QLabel#sectionTitle { color: #dceaf3; font-size: 15px; font-weight: bold; }
            QLabel#muted { color: #a4bbc9; }
            QLabel#status { color: #6df1ab; font-weight: bold; }
            QPushButton { background: #162638; padding: 8px; border: 1px solid #36516b; border-radius: 5px; }
            QPushButton:checked { background: #164834; border: 1px solid #42dc92; color: #a5ffcc; font-weight: bold; }
            QPushButton:hover { border-color: #64b6d7; }
            QComboBox, QSpinBox { background: #182d3d; padding: 5px; border: 1px solid #375168; }
            QTableWidget { background: #091521; alternate-background-color: #132537; gridline-color: #254052; border: 1px solid #2c455b; }
            QHeaderView::section { background: #213549; color: #e1eef5; padding: 5px; border: 1px solid #345066; }
            QTextEdit { background: #091521; border: 1px solid #2d485d; }
        ''')

    def _make_table(self):
        table = QTableWidget(0, 7)
        table.setHorizontalHeaderLabels(['ID', 'Distancia (m)', 'Velocidad (m/s)', 'SNR (dB)', 'Azimut (°)', 'Estado', 'Edad (s)'])
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.verticalHeader().hide()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.itemSelectionChanged.connect(self._target_selected)
        return table

    def _build_main_dashboard(self):
        page = QWidget()
        grid = QGridLayout(page)
        grid.setContentsMargins(0, 0, 0, 0)
        self.main_position = PositionDisplay()
        self.main_wave = SignalDisplay('wave')
        self.main_spectrum = SignalDisplay('spectrum')
        self.main_log = QTextEdit()
        self.main_log.setReadOnly(True)
        widgets = (
            ('Posición · rango y azimut', self.main_position, 0, 0),
            ('Onda I/Q · I en cian, Q en verde', self.main_wave, 0, 1),
            ('Bitácora de objetos', self.main_log, 1, 0),
            ('Espectro · magnitud en dBFS', self.main_spectrum, 1, 1),
        )
        for title, widget, row, col in widgets:
            box, layout = panel(title)
            widget.setMinimumHeight(165)
            layout.addWidget(widget, 1)
            grid.addWidget(box, row, col)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        self.pages.addWidget(page)

    def _build_home(self):
        page = QWidget()
        layout = QHBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        box, bl = panel('Vista de detecciones')
        self.range_display = PositionDisplay()
        bl.addWidget(self.range_display, 1)
        bl.addWidget(info_label('INTERPRETACIÓN:', 'Rango y azimut de las detecciones sintéticas. Los paquetes RADR aparecen en la tabla.'))
        layout.addWidget(box, 7)
        right = QVBoxLayout()
        targets_box, targets_layout = panel('Última detección por ID (ROM de prueba)')
        self.table = self._make_table()
        targets_layout.addWidget(self.table)
        right.addWidget(targets_box, 6)
        stats_box, stats_l = panel('Diagnóstico Ethernet')
        self.stats = QLabel()
        self.stats.setWordWrap(True)
        stats_l.addWidget(self.stats)
        right.addWidget(stats_box, 2)
        log_box, log_l = panel('Bitácora del sistema')
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_l.addWidget(self.log_text)
        right.addWidget(log_box, 5)
        layout.addLayout(right, 4)
        self.pages.addWidget(page)

    def _view_page(self, title, note, view):
        page = QWidget()
        layout = QVBoxLayout(page)
        box, bl = panel(title)
        bl.addWidget(info_label('', note))
        bl.addWidget(view, 1)
        layout.addWidget(box)
        self.pages.addWidget(page)

    def _build_wave(self):
        self.wave_view = SignalDisplay('wave')
        self._view_page('Onda I/Q · muestras sintéticas de la FPGA',
                        'I en cian · Q en verde · amplitud normalizada', self.wave_view)

    def _build_spectrum(self):
        self.spectrum_view = SignalDisplay('spectrum')
        self._view_page('Espectro I/Q · magnitud en dBFS',
                        'DFT calculada en el HMI sobre el bloque recibido',
                        self.spectrum_view)

    def _build_position(self):
        self.position_view = PositionDisplay()
        self._view_page('Posición en planta · rango y azimut',
                        'Datos sintéticos · 0° al frente · sentido positivo horario',
                        self.position_view)

    def _build_history(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        box, bl = panel('Historial de detecciones y eventos')
        self.history_info = QLabel('Sin datos todavía')
        bl.addWidget(self.history_info)
        export = QPushButton('Guardar historial de detecciones en CSV')
        export.clicked.connect(self.export_csv)
        bl.addWidget(export)
        self.history_log = QTextEdit()
        self.history_log.setReadOnly(True)
        bl.addWidget(self.history_log, 1)
        layout.addWidget(box)
        self.pages.addWidget(page)

    def _build_settings(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        box, bl = panel('Configuración de visualización y recepción')
        line = QHBoxLayout()
        line.addWidget(QLabel('Rango visible (m):'))
        self.range_spin = QSpinBox()
        self.range_spin.setRange(10, 100000)
        self.range_spin.setSingleStep(20)
        self.range_spin.setValue(int(self.max_range))
        self.range_spin.valueChanged.connect(self._range_changed)
        line.addWidget(self.range_spin)
        line.addStretch()
        bl.addLayout(line)
        bl.addWidget(info_label('Puerto UDP:', str(self.port)))
        bl.addWidget(info_label('Protocolo:', 'RADR · 24 bytes · big endian'))
        bl.addWidget(info_label('Refresco de pantalla:', '10 Hz (QTimer)'))
        bl.addWidget(info_label('Recepción:', 'QSocketNotifier no bloqueante'))
        bl.addWidget(info_label('Caducidad de detección:', '{:.0f} s'.format(ACTIVE_TIMEOUT_S)))
        bl.addStretch()
        layout.addWidget(box)
        self.pages.addWidget(page)

    def show_page(self, index):
        self.pages.setCurrentIndex(index)
        for i, btn in enumerate(self.navbuttons):
            btn.setChecked(i == index)

    def _range_changed(self, value):
        self.max_range = float(value)

    def _open_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setblocking(False)
            self.sock.bind(('0.0.0.0', self.port))
            self.notifier = QSocketNotifier(self.sock.fileno(), QSocketNotifier.Read, self)
            self.notifier.activated.connect(self.read_udp)
        except OSError as e:
            self.log_event('ERROR: no se pudo abrir UDP {}: {}'.format(self.port, e))
            QMessageBox.critical(self, 'Error de UDP', str(e) + '\nCierra otros receptores en el puerto.')

    def read_udp(self, *args):
        # Procesamiento por lotes: nunca esperar dentro del hilo de Qt.
        if self.sock is None:
            return
        for unused in range(256):
            try:
                data, address = self.sock.recvfrom(2048)
            except (BlockingIOError, InterruptedError):
                break
            except OSError as e:
                self.log_event('Error de recepción UDP: {}'.format(e))
                break
            try:
                is_scene = data[:4] == b'RSC1'
                is_iq = is_scene or data[:4] == b'RADQ'
                d = decode_iq(data) if is_iq else decode_packet(data)
            except (ValueError, struct.error) as e:
                self.invalid += 1
                if self.invalid <= 3 or self.invalid % 100 == 0:
                    self.log_event('Paquete inválido: {}'.format(e))
                continue
            self.rx += 1
            now = time.monotonic()
            d['recv_mono'] = now
            d['recv_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            if self.last_seq is not None:
                diff = (d['seq'] - self.last_seq) & 0xFFFFFFFF
                if diff == 0:
                    self.duplicates += 1
                elif 1 < diff < 0x80000000:
                    self.missing += diff - 1
                    self.log_event('Salto de secuencia: {} paquetes posiblemente perdidos'.format(diff - 1))
            self.last_seq = d['seq']
            self.last_packet = now
            if not is_iq and d['reserved'] == 0xA5:
                self.scene_rows[d['seq']] = d
                if len(self.scene_rows) > 12:
                    del self.scene_rows[next(iter(self.scene_rows))]
                continue
            if is_iq:
                if is_scene:
                    keys = [(d['seq']-i) & 0xFFFFFFFF for i in (4,3,2,1)]
                    rows = [self.scene_rows.pop(k, None) for k in keys]
                    if any(row is None for row in rows) or {row['id'] for row in rows} != {1,2,3,4}:
                        self.log_event('Escena incompleta · se conserva la última escena completa')
                        continue
                    active = {row['id']: row for row in rows if row['state']}
                    self._replace_targets(active)
                    self.history.extend(row.copy() for row in active.values())
                self.last_iq = now
                times = [i*1e6/d['fs'] for i in range(len(d['iq']))]
                wave = ((times, [x.real for x in d['iq']]),
                        (times, [x.imag for x in d['iq']]))
                freqs, levels = spectrum(d)
                self._set_signal_views(wave, (([f/1000 for f in freqs], levels),))
                continue
            tid = d['id']
            if not d['state']:
                self._remove_target(tid, 'salida indicada en el paquete')
                continue
            first = tid not in self.targets
            self.targets[tid] = d
            self.history.append(d.copy())
            if first:
                self._log_detection(d)

    def _set_signal_views(self, wave, frequency):
        for view in (self.wave_view, self.main_wave):
            view.set_series(wave)
        for view in (self.spectrum_view, self.main_spectrum):
            view.set_series(frequency)

    def _log_detection(self, target):
        angle = target['azimuth_deg']
        azimuth = '—' if angle is None else '{:+.2f}°'.format(angle)
        self.log_event('Detección · ID {} · {:.2f} m · azimut {} · {:+.2f} m/s'.format(
            target['id'], target['range_m'], azimuth, target['velocity_mps']))

    def _remove_target(self, target_id, reason):
        target = self.targets.pop(target_id, None)
        if target is not None:
            self.log_event('Salida · ID {} · {} · último rango {:.2f} m'.format(
                target_id, reason, target['range_m']))

    def _replace_targets(self, active):
        before = set(self.targets)
        for tid in sorted(before - set(active)):
            self._remove_target(tid, 'ausente en la escena')
        for tid in sorted(set(active) - before):
            self._log_detection(active[tid])
        self.targets = active

    def log_event(self, message):
        stamp = datetime.now().strftime('%H:%M:%S')
        event_text = '[{}] {}'.format(stamp, message)
        self.events.appendleft(event_text)
        self.main_log.setPlainText('\n'.join(list(self.events)[:80]))
        if hasattr(self, 'log_text'):
            self.log_text.setPlainText('\n'.join(list(self.events)[:80]))
        if hasattr(self, 'history_log'):
            self.history_log.setPlainText('\n'.join(list(self.events)[:250]))

    def _target_selected(self):
        items = self.table.selectedItems()
        if items:
            try:
                self.selected_id = int(items[0].text())
            except (ValueError, IndexError):
                pass

    def refresh_display(self):
        now = time.monotonic()
        expired = [tid for tid, d in self.targets.items() if now - d['recv_mono'] > ACTIVE_TIMEOUT_S]
        for tid in expired:
            self._remove_target(tid, 'sin actualizaciones recientes')
        connected = self.last_packet is not None and now - self.last_packet < 2.0
        state = 'RECIBIENDO' if connected else 'SIN DATOS'
        self.status_label.setText('UDP {}  |  RX {}  |  faltantes {}  |  inválidos {}'.format(
            state, self.rx, self.missing, self.invalid))
        self.stats.setText(
            'Puerto UDP: {}\nPaquetes válidos: {}\nFaltantes estimados: {}\n'
            'Duplicados: {}\nInválidos: {}\nIDs recientes: {}\n'
            'Edad último paquete: {}'.format(
                self.port, self.rx, self.missing, self.duplicates, self.invalid,
                len(self.targets),
                '{:.2f} s'.format(now - self.last_packet) if self.last_packet is not None else 'N/D'))
        self.range_display.set_data(self.targets, self.max_range, self.selected_id)
        self.position_view.set_data(self.targets, self.max_range, self.selected_id)
        self.main_position.set_data(self.targets, self.max_range, self.selected_id)
        if getattr(self, 'last_iq', None) is not None and now-self.last_iq > 2:
            self.last_iq = None
            self._set_signal_views((), ())
        # Mantener la selección al repoblar la tabla.
        selected = self.selected_id
        self.table.blockSignals(True)
        self.table.setRowCount(len(self.targets))
        for row, tid in enumerate(sorted(self.targets)):
            d = self.targets[tid]
            vals = [str(tid), '{:.2f}'.format(d['range_m']),
                    '{:+.2f}'.format(d['velocity_mps']), '{:.1f}'.format(d['snr_db']),
                    '—' if d['azimuth_deg'] is None else '{:+.2f}'.format(d['azimuth_deg']),
                    str(d['state']), '{:.2f}'.format(now-d['recv_mono'])]
            for col, val in enumerate(vals):
                self.table.setItem(row, col, QTableWidgetItem(val))
            if tid == selected:
                self.table.selectRow(row)
        self.table.blockSignals(False)
        if selected is None and self.targets:
            self.selected_id = sorted(self.targets)[0]
        self.history_info.setText('{} registros en memoria (máximo {}). '
                                  'Los datos son sintéticos.'.format(len(self.history), HISTORY_LIMIT))

    def export_csv(self):
        if not self.history:
            QMessageBox.information(self, 'Sin registros', 'No hay registros para exportar.')
            return
        name, unused = QFileDialog.getSaveFileName(self, 'Guardar detecciones',
            'radarlink_detecciones.csv', 'CSV (*.csv)')
        if not name:
            return
        columns = ['recv_time', 'seq', 'ticks', 'id', 'range_m', 'velocity_mps',
                   'snr_db', 'azimuth_deg', 'state', 'reserved']
        try:
            with open(name, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(self.history)
            self.log_event('CSV guardado: {} registros'.format(len(self.history)))
        except (OSError, IOError) as e:
            QMessageBox.warning(self, 'Error guardando CSV', str(e))

    def closeEvent(self, event):
        if self.notifier is not None:
            self.notifier.setEnabled(False)
        if self.sock is not None:
            self.sock.close()
        super(RadarWindow, self).closeEvent(event)


def main():
    parser = argparse.ArgumentParser(description='RadarLink HMI para Nexys Video')
    parser.add_argument('--port', type=int, default=PORT)
    parser.add_argument('--range', type=int, default=850)
    args = parser.parse_args()
    app = QApplication(sys.argv[:1])
    window = RadarWindow(args.port, args.range)
    window.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
