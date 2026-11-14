# Fundamentos de radar coherente

## Cadena de señal

Transmisión RF → propagación → eco → amplificación y mezcla → I/Q en banda base → ADC → procesamiento.

La frecuencia de portadora (por ejemplo, 2,45 GHz) **no es la frecuencia de reloj de la FPGA**. Ésta procesa muestras I/Q digitalizadas por un front-end RF.

## Distancia y FMCW

Para una chirp lineal de pendiente `S = B/T_chirp`, una reflexión estacionaria monostática tiene aproximadamente `f_b = (2 R / c) S`. La resolución ideal en distancia resulta:

$$\Delta R = \frac{c}{2B}$$

Para `B = 10 MHz`, `ΔR ≈ 15 m`. Resolución no significa precisión absoluta, y los objetivos móviles requieren tratamiento del Doppler y de su acoplamiento con la frecuencia de batido.

## Velocidad y Doppler

En radar monostático, `f_D = 2v_r/λ` (signo según convención). La estimación puede realizarse mediante diferencias de fase entre chirps. La resolución y ambigüedad Doppler dependen de la cadencia y la duración de la ventana de observación.

## Integración coherente

Una mejora ideal `10 log10(N)` dB tras integrar `N` observaciones solo es alcanzable con sincronización adecuada y ruido no correlacionado. La integración requiere compensar el movimiento y controlar ruido de fase, errores de reloj y pérdidas numéricas.

## Detección

CFAR permite ajustar umbrales con estimaciones locales de ruido y clutter. La especificación final debe fijar `P_d` y `P_fa`, además de SNR.

## Referencias a documentar

Incorporar referencias primarias a teoría de radar, datasheets y notas de aplicación, incluyendo versión, fecha y URL de los documentos efectivamente utilizados.

[Volver al índice técnico](../README.md)
