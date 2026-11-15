# Procesamiento digital en FPGA

```mermaid
flowchart LR
 A[Entrada I/Q] --> B[Buffer y timestamp]
 B --> C[DC removal / filtros]
 C --> D[Range FFT]
 D --> E[Doppler FFT]
 E --> F[CFAR]
 F --> G[Detecciones Ethernet]
```

## Diseño modular previsto

| Módulo futuro | Propósito | Estado |
|---|---|---|
| `iq_source_sim` | Reproducir datos sintéticos | Pendiente |
| `iq_capture` | Captura I/Q y control de dominios de reloj | Pendiente |
| `fir_filter` | Filtrado en punto fijo | Pendiente |
| `range_fft` | Compresión y mapa de distancia | Pendiente |
| `doppler_fft` | Procesamiento entre chirps | Pendiente |
| `cfar_detector` | Umbral adaptativo | Pendiente |
| `telemetry_tx` | Paquetizado Ethernet | Pendiente |

No se han escogido formatos Q, longitudes FFT, frecuencia de reloj ni la interfaz ADC. Los valores deben proceder del diseño RF y de simulaciones cuantitativas.

## Métricas

Error numérico frente a Python/MATLAB, LUT, FF, BRAM, DSP, frecuencia máxima, latencia por trama, caudal sostenido y tasa de pérdida de muestras.

## Integración coherente explícita

La FFT Doppler integra coherentemente muestras de cada bin de rango entre chirps. No añadir su ganancia nuevamente como un bloque independiente sobre las mismas muestras. Acumulación adicional entre tramas: pendiente de justificar y compensar movimiento/fase.

[Contrato de interfaces](interfaces.md) · [Plan de simulación](../../simulation/PLAN.md)

[Volver al índice técnico](../README.md)

## Estudio de formatos numéricos

[FFT en punto fijo, con esquemas](fft-punto-fijo.md). Hay un contrato inicial propuesto de formatos y escalado; la frase anterior sobre formatos no escogidos describe la situación previa y la selección definitiva sigue pendiente. La FFT flotante de S1 no se convierte en fija por cuantizar solo la entrada.
