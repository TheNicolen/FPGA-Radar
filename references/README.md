# Referencias técnicas

[Inicio](../README.md) · [Índice técnico](../docs/README.md)

Fuentes primarias consultadas el 2026-11-14. Las páginas web son mutables; antes de fijar pines o compatibilidad descargar la revisión apropiada y registrar fecha/revisión/hash. No se han validado esquemas de una combinación concreta de placas.

| ID | Fuente | Uso y límites |
|---|---|---|
| REF-001 | Digilent, [Nexys Video Reference Manual](https://digilent.com/reference/_media/nexys-video%3Anexys_video_rm.pdf) | Referencia de placa; revisión exacta pendiente de fijar para implementación |
| REF-002 | Digilent, [Nexys Video Master XDC](https://github.com/Digilent/digilent-xdc/blob/master/Nexys-Video-Master.xdc) | Fuente de restricciones; fijar commit y verificar esquema antes de usar |
| REF-003 | Analog Devices, [AD-FMCOMMS3-EBZ](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/EVAL-AD-FMCOMMS3-EBZ.html) | Identifica módulo de evaluación AD9361; no prueba compatibilidad Nexys Video |
| REF-004 | Analog Devices, [ADALM-PLUTO](https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/adalm-pluto.html) | Arquitectura propia AD9363/Zynq; no equivale a enlace FMC de Nexys Video |
| REF-005 | Analog Devices, [Introducción a placas AD936x](https://developer.analog.com/docs/system-level/solutions/reference-designs/fmcomms2/common/introduction_to_ad9361_ad9364/) | Distingue transceptores, placas y sus interfaces |

La teoría de radar y dimensiones de cantenna proceden del paquete inicial: requieren completar bibliografía académica y revisión independiente. Los resultados del script de enlace verifican aritmética del modelo, no validez física de sus supuestos. Normativa SUBTEL, precios actuales, herramientas y documentación específica Jetson pendientes de estudio; no se declara conformidad ni disponibilidad comercial.
