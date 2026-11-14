# Requisitos y trazabilidad

| ID | Requisito | Estado | Verificación prevista |
|---|---|---|---|
| SYS-001 | Plataforma de procesamiento: Nexys Video | Propuesto | Síntesis y timing en Vivado |
| SYS-002 | Control y visualización: Jetson Nano | Propuesto | Demo Ethernet |
| SYS-003 | Detección aspiracional de vehículo hasta 1 km | No demostrado | Pruebas de campo autorizadas y `P_d`/`P_fa` |
| SYS-004 | Presupuesto RF/accesorios < $300.000 CLP | Restricción | Inventario, cotizaciones y gastos |
| RF-001 | Receptor I/Q coherente | Pendiente | Ensayos de sincronismo y fase |
| RF-002 | Banda RF y potencia legalmente admisibles | Pendiente | Revisión normativa y permisos |
| RF-003 | Antena RX: reflector disponible 46 × 46 cm | Parcial | Medición geométrica y de patrón |
| DSP-001 | Procesamiento de distancia (FFT) | Pendiente | Pruebas con datos sintéticos |
| DSP-002 | Procesamiento Doppler | Pendiente | Pruebas con objetivos móviles simulados |
| DSP-003 | Detección CFAR | Pendiente | Curvas `P_d`/`P_fa` |
| IF-001 | Enlace FPGA ↔ Jetson | Pendiente | Prueba de caudal y pérdida de paquetes |
| DOC-001 | Bitácora verificable por avance | Iniciado | Plantillas y registros versionados |

**Pendientes de cuantificar:** tasa de actualización, ancho de banda del chirp, intervalo de velocidades, precisión, resolución angular, latencia admisible, consumo eléctrico y límites de tamaño/peso.

[Volver al índice técnico](../README.md)

## Trazabilidad de la siguiente etapa

| Requisitos | Plan y evidencia requerida | Estado de validación |
|---|---|---|
| SYS-003 | [Cálculo de enlace](../../simulation/reports/2026-11-14-calculo-enlace.md), luego F5 | Cálculo disponible; 1 km no demostrado |
| DSP-001/002/003 | [SIM-001 a SIM-007](../../simulation/PLAN.md) y testbenches RTL | Sin ejecución FMCW/RTL |
| SYS-001 | [Plan FPGA](../../fpga/README.md), timing/recursos | Sin síntesis |
| SYS-002, IF-001 | [Interfaces](../06-procesamiento/interfaces.md) y pruebas Jetson | Sin implementación |
| RF-001 | [Matriz de compatibilidad](../../hardware/rf/compatibilidad.md) y loopback | Pendiente |
| SYS-004 | [BOM](../../hardware/BOM.md) | Sin cotizaciones |
| DOC-001 | [Bitácora](../../progress/README.md) y comprobador de enlaces | Preparación local |

RF-002 y RF-003 requieren evidencia regulatoria y mediciones físicas respectivamente. SYS-001/002 quedan fijados como plataformas objetivo por la solicitud actual; esto no cambia su estado de validación física.
