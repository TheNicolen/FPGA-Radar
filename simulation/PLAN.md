# Plan de simulación FMCW

[Inicio](../README.md) · [Simulación](README.md) · [Hoja de ruta](../ROADMAP.md)

**[PROPUESTO; NO EJECUTADO]** Modelo de banda base con chirps coherentes y objetivos sintéticos. El cálculo de enlace disponible es un paso previo.

## Parámetros que deben congelarse por ejecución

fc_hz, sweep_bandwidth_hz, chirp_duration_s, chirp_interval_s (incluye tiempo muerto), sample_rate_hz, samples_per_chirp, chirps_per_frame, ventana, seed, ruido, RCS, amplitudes, rangos, velocidades y convención de fase. No confundir ancho de barrido RF con ancho de ruido IF.

Para el modelo monostático: S=B/T; tau=2R/c; fD=2v/lambda. Aproximación de batido f_b=S*tau+fD según convención de mezcla. La señal discreta debe preservar fase entre chirps. Declarar aproximación stop-and-hop y comprobar migración de celda durante la CPI. Verificar tau<T y límites de muestreo; no modelar alcance ilimitado con una sinusoide sin retardo.

Resolución ideal de rango c/(2B); resolución Doppler aproximada lambda/(2*M*Tr); límite no ambiguo de velocidad ±lambda/(4*Tr). Son relaciones ideales que deben contrastarse con ventana, duración efectiva y muestreo. Zero-padding interpola bins; no mejora resolución física.

## Casos y aceptación propuesta

| ID | Caso | Criterio previo a declarar aprobado |
|---|---|---|
| SIM-001 | Un blanco estático sin ruido | Pico dentro de medio bin en escenario alineado; signo y ejes correctos |
| SIM-002 | Blanco móvil y velocidades ± | Error menor o igual a un bin; signo documentado |
| SIM-003 | Dos blancos | Separación acorde a resolución y ventana; registrar casos no resueltos |
| SIM-004 | Ruido sin blancos | Pfa empírica con denominador de celdas evaluadas e intervalo de confianza |
| SIM-005 | Monte Carlo con blancos | Pd vs SNR/RCS, número de ensayos y criterio de asociación definidos |
| SIM-006 | Saturación y punto fijo | Error/tolerancia por etapa, overflow y pérdida de Pd cuantificados |
| SIM-007 | Fuga TX/RX, clutter y ruido de fase | Barridos y límites de validez; sin extrapolar a campo |

CFAR inicial por decidir: CA-CFAR sobre potencia lineal. Fijar celdas de entrenamiento/guarda, bordes y Pfa objetivo. Si se usa alpha=N*(Pfa**(-1/N)-1), documentar que supone muestras independientes exponenciales; ventanas y correlación pueden invalidar la Pfa nominal. No cerrar el hito solo porque se genera un mapa coloreado.

## Reproducibilidad

Guardar configuración, seed, versiones, commit, verdad sintética y checksum de vectores. Separar salida flotante, cuantizada y RTL; tablas y gráficos deben llevar [SIMULADO]. Resultados grandes en almacenamiento privado con manifiesto; resúmenes pequeños revisados en reports/.

## Avance 2026-11-14

La [primera referencia MATLAB](reports/2026-11-14-matlab-estudio-inicial.md) ya fue ejecutada. Cubre casos básicos de rango/Doppler, blancos separados, cuantización de entrada y CFAR IID aislado. SIM-004/005 completos, punto fijo interno y degradaciones RF siguen pendientes. El encabezado inicial describe el plan previo a esta ejecución.
