# Contratos digitales propuestos

[Índice](../README.md) · [Pipeline](pipeline.md)

**[PROPUESTO]** Contrato de laboratorio independiente del front-end. No es un pinout físico.

| Interfaz | Contenido | Pendiente antes de RTL |
|---|---|---|
| IQ → filtro | I y Q signed, valid/ready, frame_id, chirp_id, sample_id | Ancho por componente, endian y escala |
| Filtro → FFT distancia | Muestras complejas, fin de chirp | Decimación, latencia y ventana |
| FFT distancia → memoria | Bin de distancia y amplitud compleja | Orden de bins, escalado y capacidad |
| Memoria → FFT Doppler | Serie coherente del mismo bin entre chirps | Número de chirps, stride y planificación |
| FFT Doppler → CFAR | Potencia lineal por celda, índices | Escala, saturación y bordes |
| CFAR → Jetson | Detecciones, frame_id, timestamp, configuración | Protocolo, unidades, versión y ancho de campos |

Transferencia solo cuando valid y ready están activos. Con valid activo y ready inactivo, mantener datos/metadatos estables. Contabilizar overflow; invalidar trama incompleta en lugar de producir una detección aparentemente válida. CDC mediante FIFO asíncrona o mecanismo verificado; no pasar buses multibit con sincronizadores individuales.

Fijar convención de signo de Doppler y orden I+jQ, origen temporal, normalización de FFT, rounding y saturación. Dimensionar almacenamiento bruto como N_muestras × N_chirps × 2 × bits_por_componente; calcular además los anchos crecientes de FFT y doble buffering. Documentar LUT/FF/BRAM/DSP y timing después de síntesis e implementación, sin prometer que el diseño cabe antes de medir.

La integración coherente está incorporada en la FFT Doppler para cada hipótesis de velocidad. Cualquier acumulación adicional entre tramas requiere compensación de fase/movimiento y una nueva evaluación de pérdidas.
