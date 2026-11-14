# Presupuesto de enlace preliminar (NO VALIDADO)

**Estado: [ESTIMADO]**. Escenario monostático equivalente de detección a 1 km; los resultados no garantizan funcionamiento en ambiente real.

## Hipótesis

| Parámetro | Valor |
|---|---:|
| Frecuencia `f` | 2,45 GHz |
| Distancia `R` | 1.000 m |
| Potencia conducida `P_t` | 0 dBm (1 mW) |
| Ganancia TX `G_t` | 15 dBi |
| Ganancia RX `G_r` | 18,85 dBi (reflector **idealizado**) |
| Sección radar equivalente `σ` | 10 m² (escenario, no mínimo) |
| Pérdidas agrupadas `L` | 6 dB |
| Figura de ruido `NF` | 6 dB |
| Ancho de banda ilustrativo `B` | 10 MHz |

## Ecuación de radar

$$P_r = \frac{P_t G_t G_r \lambda^2 \sigma}{(4\pi)^3R^4L}, \quad \lambda=\frac{c}{f}$$

Con las hipótesis anteriores `λ ≈ 0,1224 m`, `P_r ≈ -133,4 dBm`. Si ambas antenas fueran 15 dBi, `P_r ≈ -137,2 dBm`.

El ruido térmico integrado en 10 MHz con NF de 6 dB es:

$$P_n\,[\mathrm{dBm}] = -174 + 10\log_{10}(10^7) +6 \approx -98\ \mathrm{dBm}.$$

La SNR previa al procesamiento sería `−35,4 dB` con el reflector idealizado. Alcanzar un objetivo de SNR postprocesamiento de 10 dB requeriría **al menos 45,4 dB de ganancia de procesamiento ideal** bajo este modelo.

**Advertencia técnica:** la banda de ruido de 10 MHz usada aquí es una referencia ilustrativa. En FMCW real, el ancho de banda de modulación no debe confundirse automáticamente con el ancho de banda de ruido de la IF ni con el tiempo de observación del filtro adaptado. El rendimiento debe recalcularse con el plan exacto de chirps, filtrado y muestreo.

## Riesgos pendientes

- RCS del vehículo desconocida y variable; evaluar al menos 1, 10 y 100 m².
- Acoplamiento TX/RX, rango dinámico y ruido de fase no cuantificados.
- Clutter del terreno y multitrayectoria no modelados.
- EIRP y permisos de emisión no determinados.
- Pérdidas de cables antes del LNA y eficiencia real del reflector por medir.
- No se dispone aún de transceptor coherente ni de mediciones de SNR.

## Criterio de aceptación futuro

Estimar `P_d` y `P_fa` en escenarios con clutter; contrastar curvas medidas vs. simuladas mediante reflectores calibrados y objetivos representativos.

[Volver al índice técnico](../README.md)
