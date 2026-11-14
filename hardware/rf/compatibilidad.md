# Matriz de compatibilidad RF

[Hardware](../README.md) · [ADR de selección](../../docs/decisiones/ADR-0002-seleccion-rf.md)

**[PENDIENTE]** No conectar AD-FMCOMMS3-EBZ a Nexys Video basándose solo en el conector FMC.

| Comprobación | Evidencia requerida | Estado |
|---|---|---|
| Mecánica y pinout | Esquemas de revisiones exactas, mapa pin a pin | Pendiente |
| Alimentaciones y VADJ | Tensiones, secuencia, corrientes y bancos FPGA | Pendiente |
| I/Q y reloj | Estándares eléctricos, pares, DDR y timing | Pendiente |
| Control | SPI, reset, GPIO y arranque | Pendiente |
| HDL y software | Portabilidad del diseño de referencia, IP y control AD9361 | Pendiente |
| Capacidad | Caudal real, buffers, recursos y sincronización | Pendiente |
| Costo | Cotización con impuestos/adaptaciones/envío | Pendiente |

ADALM-PLUTO integra su propio SoC; usarlo en banco no demuestra integración digital con Nexys Video. AD9361 es un transceptor, no una placa completa. Módulos Doppler económicos no sustituyen la arquitectura FMCW sin demostrar acceso coherente y rango.

Fuentes y enlaces oficiales: [registro de referencias](../../references/README.md). No se ha validado compatibilidad física o funcional.
