# Índice técnico

| Apartado | Documento | Estado |
|---|---|---|
| 01 | [Introducción y alcance](01-introduccion/objetivos-y-alcance.md) | Borrador |
| 02 | [Principios de radar](02-fundamentos/principios-radar.md) | Borrador |
| 02 | [Presupuesto de enlace](02-fundamentos/presupuesto-enlace.md) | Cálculo ilustrativo |
| 03 | [Requisitos verificables](03-requisitos/requisitos.md) | Inicial |
| 04 | [Arquitectura](04-arquitectura/arquitectura-general.md) | Propuesta |
| 05 | [Reflector DirecTV](05-antenas/reflector-directv.md) | Geometría parcial |
| 05 | [Cantenna](05-antenas/alimentador-cantenna.md) | Estudio preliminar |
| 06 | [Procesamiento en FPGA](06-procesamiento/pipeline.md) | Plan |
| 07 | [Verificación](07-implementacion/verificacion.md) | Plan |
| 08 | [Protocolo experimental](08-experimentos/protocolo.md) | Plan |
| ADR | [Registro de decisiones](decisiones/README.md) | Abierto |

## Convenciones

- **[MEDIDO]:** dato obtenido experimentalmente y respaldado por evidencia.
- **[SIMULADO]:** resultado reproducible del modelo computacional.
- **[ESTIMADO]:** cálculo o supuesto analítico no validado.
- **[PROPUESTO]:** decisión de diseño pendiente de cierre.
- **[PENDIENTE]:** incógnita o requisito no resuelto.

Enlaces entre documentación, archivos RTL, scripts y ensayos deben ser relativos al archivo que contiene el enlace.

## Preparación del desarrollo

- [00 — Evidencia y trazabilidad](00-metodologia/evidencia.md)
- [06 — Contratos digitales](06-procesamiento/interfaces.md)
- [07 — Inicio rápido](07-implementacion/inicio-rapido.md)
- [Plan de simulación FMCW](../simulation/PLAN.md)
- [Inicio del proyecto](../README.md)

La política de evidencia amplía las etiquetas del paquete original separando explícitamente teoría e hipótesis. Los enlaces se resuelven respecto al archivo que los contiene.

- [Procedencia y preservación del paquete](00-metodologia/procedencia.md)

- [Frecuencias y modelo MATLAB](06-procesamiento/frecuencias-y-modelo-matlab.md)
