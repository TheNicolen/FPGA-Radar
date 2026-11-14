# Frecuencias, arquitectura de muestreo y modelo MATLAB

[Índice](../README.md) · [Laboratorio MATLAB](../../simulation/matlab/README.md)

## Cuatro magnitudes distintas

| Magnitud | Valor inicial de estudio | Interpretación |
|---|---:|---|
| Portadora fc | 2,45 GHz | Frecuencia RF, candidata y no definitiva |
| Barrido B | 20 MHz | Determina resolución ideal, no reloj FPGA |
| Muestreo Fs | 2 MS/s complejas | IF después de dechirp y filtrado antialias |
| Reloj digital | 100 MHz | Objetivo inicial para RTL, no Fmax demostrado |

El manual Digilent rev. A (17-06-2015), sección 5, documenta oscilador de 100 MHz. Esa referencia no prueba que cualquier pipeline cierre timing a 100 MHz: deben verificarse versión de placa, constraints, CDC, implementación y reportes de Vivado. Fuente: [manual oficial](https://digilent.com/reference/_media/nexys-video%3Anexys_video_rm.pdf).

## Restricción esencial del front-end

El modelo parte de la IF ya dechirpeada. **Un AD9361 o PLUTO no entrega automáticamente esa señal FMCW de batido:** si entrega el eco I/Q con ancho de banda del chirp, la entrada puede necesitar al menos el ancho de banda complejo B más margen (por ejemplo, estudiar 25 MS/s para B=20 MHz), mezcla con la referencia de chirp, filtro y decimación. Eso implica 800 Mbit/s brutos con I/Q de 16 bits a 25 MS/s, frente a 64 Mbit/s a 2 MS/s; además hace falta generar/transmitir el chirp y sincronizarlo.

Alternativas abiertas: dechirp analógico antes de ADC, o digital a tasa alta seguido de decimación. No se valida ninguna con este modelo. Fs=2 MS/s NO sirve para digitalizar directamente una portadora de 2,45 GHz ni un eco complejo de 20 MHz sin procesamiento previo. Filtro/decimación y rechazo de alias son tareas pendientes.

## Perfil candidato para probar matemáticas

B=20 MHz; duración de chirp 256 us; repetición 300 us; adquisición desde 8 us durante 240 us; 480 muestras por chirp y 128 chirps. FFT de rango de 512 puntos (32 ceros de relleno). El tiempo inicial evita mezclar el eco del chirp anterior para blancos hasta 1 km. La observación usa solo parte del barrido: resolución efectiva ideal c/(2*S*Tobs), distinta de c/(2*B). La ventana Hann ensancha el lóbulo; el relleno con ceros solo interpola.

La convención es x=exp(j*2*pi*((S*tau+fD)*t+fD*m*Tr+fase_constante)), fD=2v/lambda; velocidad positiva denota aproximación. Tras FFT: R_corregido=c*(fb-fD)/(2*S). No mezclar esta convención con una función de dechirp que invierta el signo sin adaptar ejes. Véase [MathWorks: estimación FMCW](https://www.mathworks.com/help/phased/ug/fmcw-range-estimation.html).

## Antena y frecuencia

Se usa G_rx=eta*4*pi*A/lambda², A=pi*0,46*0,46/4, eficiencia hipotética 0,55. Un reflector disponible se asigna a RX; la antena TX de 15 dBi es un supuesto independiente. No se presupone tener dos reflectores.

Con apertura RX y ganancia TX fijas, G_rx*lambda² es constante: subir frecuencia NO aumenta por sí solo Pr en esta comparación ideal, aunque crezca la ganancia RX en dBi. Si TX también tiene apertura fija, el resultado cambia; eso corresponde a otro hardware. RCS, eficiencia, pérdidas, polarización, haz y regulación pueden variar con frecuencia. Los barridos a 2,4/2,45/5,8 GHz no aprueban operación en esas bandas ni reutilización del mismo alimentador.

## Qué matemática llevar a FPGA

Entrada/coherencia y filtrado → ventana → FFT distancia → buffer y transposición → ventana/FFT Doppler → potencia I²+Q² → CFAR → coordenadas. El estudio implementa referencia flotante desde IF, cuantización de entrada y CFAR 1D aislado. Faltan filtros reales, FFT bit-exact, crecimiento de palabra, política de escalado, CFAR 2D, Monte Carlo Pd(SNR), control de saturación por etapa y RTL.

El conteo de mariposas radix-2 es orientativo; no incluye ancho de memoria, latencias de multiplicadores, stalls ni recursos de IP. No es evidencia de que el pipeline quepa o termine a tiempo.
