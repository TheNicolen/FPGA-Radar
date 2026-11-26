"""Qt waveform, complex spectrum and range/azimuth views."""
import math
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QWidget

BG = QColor('#0b121c')
GRID = QColor('#2b465a')
TEXT = QColor('#b6c9d8')
CYAN = QColor('#59d5f4')
GREEN = QColor('#42e99a')


class SignalDisplay(QWidget):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.series = ()
        self.setMinimumHeight(240)

    def set_series(self, series):
        self.series = series
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), BG)
        r = QRectF(self.rect()).adjusted(65, 22, -24, -48)
        p.setPen(TEXT)
        if not self.series or r.width() <= 0:
            p.drawText(self.rect(), Qt.AlignCenter, 'Esperando un bloque I/Q RADQ de la FPGA')
            return
        waveform = self.mode == 'wave'
        ymin, ymax = (-1, 1) if waveform else (-100, 6)
        x0, x1 = self.series[0][0][0], self.series[0][0][-1]
        def point(x, y):
            return QPointF(r.left()+r.width()*(x-x0)/(x1-x0),
                           r.bottom()-r.height()*(y-ymin)/(ymax-ymin))
        for j in range(5):
            y = ymin+(ymax-ymin)*j/4
            p.setPen(GRID)
            p.drawLine(point(x0,y), point(x1,y))
            p.setPen(TEXT)
            p.drawText(QPointF(7,point(x0,y).y()+4), '{:.1f}'.format(y))
            x=x0+(x1-x0)*j/4
            p.drawText(QPointF(point(x,ymin).x()-14,r.bottom()+17), '{:.1f}'.format(x))
        p.drawText(QRectF(r.left(),r.bottom()+23,r.width(),20),Qt.AlignCenter,
                   'Tiempo dentro del bloque (µs)' if waveform else 'Frecuencia de banda base (kHz)')
        for i,(xs,ys) in enumerate(self.series):
            p.setPen(QPen((CYAN,GREEN)[i],2))
            for j in range(1,len(xs)):
                p.drawLine(point(xs[j-1],ys[j-1]),point(xs[j],ys[j]))


class PositionDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.targets = {}
        self.max_range = 1
        self.selected = None
        self.setMinimumHeight(240)

    def set_data(self, targets, max_range, selected):
        self.targets = targets
        self.max_range = max(1, max_range)
        self.selected = selected
        self.update()

    def paintEvent(self, event):
        p=QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(),BG)
        origin=QPointF(self.width()/2,self.height()/2)
        radius=min(self.width(),self.height())/2-28
        if radius<=0:
            return
        p.setPen(GRID)
        for j in range(1,5):
            rr=radius*j/4
            p.drawEllipse(origin,rr,rr)
            p.drawText(QPointF(origin.x()+6,origin.y()-rr+16),'{:.0f} m'.format(self.max_range*j/4))
        p.drawLine(QPointF(origin.x()-radius,origin.y()),QPointF(origin.x()+radius,origin.y()))
        p.drawLine(QPointF(origin.x(),origin.y()-radius),QPointF(origin.x(),origin.y()+radius))
        p.setPen(TEXT)
        p.drawText(QPointF(origin.x()+6,origin.y()-radius-6),'0° · frente')
        n=0
        for tid,d in self.targets.items():
            angle=d.get('azimuth_deg')
            if angle is None or d['range_m']>self.max_range:
                continue
            a=math.radians(angle)
            rr=radius*d['range_m']/self.max_range
            pt=QPointF(origin.x()+rr*math.sin(a),origin.y()-rr*math.cos(a))
            p.setPen(GREEN if tid==self.selected else CYAN)
            p.drawEllipse(pt,5,5)
            p.drawText(QPointF(pt.x()+9,pt.y()-7),'ID {} · {:+.2f}°'.format(tid,angle))
            n+=1
        if not n:
            p.setPen(TEXT)
            p.drawText(QRectF(10,self.height()-26,self.width()-20,22),Qt.AlignCenter,
                       'Sin detecciones con azimut dentro del rango mostrado')
