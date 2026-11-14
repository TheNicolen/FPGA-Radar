# Primer laboratorio MATLAB: antena, enlace y DSP

[Inicio](../../README.md) · [Simulación](../README.md) · [Informe](../reports/2026-11-14-matlab-estudio-inicial.md)

**Estado:** ejecutado en MATLAB R2024b Update 9; ocho grupos de aserciones aprobados y resultados contrastados con referencia independiente. Consultar el informe de ejecución. No hay mediciones ni validación de alcance físico.

## Ejecutar en MATLAB

Desde la raíz del repositorio:

```matlab
addpath('simulation/matlab');
p = radar_config();
q = fmcw_parameters(p);
a = antenna_link(p,1000);
test_radar();
run_study();
```

Requiere MATLAB con fft, tablas y exportgraphics; diseñado para R2024b, sin Radar Toolbox ni Fixed-Point Designer. `run_study` escribe en simulation/results/matlab (ignorado por Git). Produce CSV de sensibilidad, resumen JSON, figuras PNG, MAT y un vector I/Q de un chirp. Para otra ubicación: `run_study('ruta_de_salida')`.

## Qué modificar

[radar_config.m](radar_config.m) centraliza supuestos. Mantener copia de configuración y seed por ejecución. Cambiar potencia, eficiencia, RCS y pérdidas antes de interpretar alcance; los valores actuales son hipótesis. El área pi*ancho*alto/4 supone una apertura elíptica proyectada equivalente: 46 × 46 cm físicos no demuestran esa apertura efectiva en el reflector offset.

## Experimentos incluidos

| Archivo | Función | Límite |
|---|---|---|
| [antenna_link.m](antenna_link.m) | Ganancia RX, enlace, SNR ideal y cruce de umbral | Modelo analítico; umbral 10 dB no implica Pd/Pfa |
| [fmcw_parameters.m](fmcw_parameters.m) | Muestreo, ambigüedad, migración, memoria y operaciones | No determina Fmax ni valida ADC |
| [synth_iq.m](synth_iq.m) | I/Q de blancos sintéticos con fase coherente | IF ya dechirpeada, retardo constante durante CPI |
| [range_doppler.m](range_doppler.m) | Hann y FFT 2D normalizada | Punto flotante; rango aparente necesita corrección Doppler |
| [quantize_iq.m](quantize_iq.m) | Entrada Q1.15 configurable | No simula aritmética fija interna de FFT |
| [ca_cfar_1d.m](ca_cfar_1d.m) | CA-CFAR en potencia lineal | No integra todavía detección 2D del mapa |
| [test_radar.m](test_radar.m) | Ocho grupos de aserciones | Ejecutar en MATLAB antes de declararlos aprobados |
| [run_study.m](run_study.m) | Barridos y figuras reproducibles | No sustituye ensayos RF |

Los blancos normalizados del mapa se usan para verificar algoritmos y NO tienen amplitud derivada del enlace de 1 km. Una figura con un blanco a 600 m no demuestra sensibilidad física a esa distancia.

La ganancia coherente se calcula con las ventanas: ((sum wr)^2/sum wr²)*((sum wd)^2/sum wd²). No multiplicar nuevamente por N*M. El ruido supone banda equivalente Fs para ruido complejo blanco. En hardware recalcular con filtros, correlación y respuesta real.

El alcance por umbral es un cruce energético ideal; puede quedar fuera del alcance configurado o de la ventana temporal. No es alcance operativo. El perfil solo se comprueba hasta 1 km; sus restricciones no se extienden automáticamente a los cruces de umbral calculados.

## Comprobación independiente

[verify_reference.py](verify_reference.py) reproduce las ecuaciones y casos en Python. Sus resultados comprueban la referencia matemática, **no prueban que los archivos .m se ejecuten correctamente**. Usa solo la biblioteca estándar de Python; la versión efectivamente utilizada queda en su salida. El comando es `python simulation/matlab/verify_reference.py` y las salidas quedan en simulation/results/python_reference.
