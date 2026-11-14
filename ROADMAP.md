# Hoja de ruta verificable

[Inicio](README.md) · [Requisitos](docs/03-requisitos/requisitos.md) · [Bitácora](progress/README.md)

Los criterios son propuestos y deben fijarse antes de los ensayos. Ninguna carpeta creada demuestra un hito técnico.

| Hito | Dependencia | Entregable y criterio de cierre | Estado |
|---|---|---|---|
| F0.0 Organización | Paquete inicial | Capítulos navegables, ADR, bitácora, convenciones y comprobación de enlaces | Estructura local verificada; remoto privado vacío inspeccionado para carga |
| F0.1 Enlace | SYS-003/004 | Cálculo reproducible, barridos RCS 1/10/100 m², sensibilidad a pérdidas y tabla de supuestos | Cálculo base disponible; barridos pendientes |
| F0.2 FMCW | F0.1 | Configuración congelada; SIM-001 a SIM-005 ejecutados; Pd/Pfa, resolución y velocidad acordadas | Pendiente |
| F1.0 Formatos e interfaces | F0.2 | Contrato I/Q, formatos Q, tolerancias, buffers y vectores con hashes | Propuesto |
| F1.1 RTL por bloque | F1.0 | Testbench autochecking, stalls/reset/overflow, comparación numérica por bloque | Pendiente |
| F1.2 Nexys Video | F1.1 | Pipeline sintético, timing cerrado al reloj elegido, recursos dentro del dispositivo y cero pérdida al caudal acordado | Pendiente |
| F2 Jetson | F1.0 | Protocolo versionado, prueba de caudal/duración acordados, contadores de pérdida y detección de secuencias faltantes | Pendiente |
| F3 Antena | Instrumentos | Geometría, S11 y patrón con incertidumbre; ganancia por método calibrado | Pendiente |
| F4 RF coherente | ADR-0002, F1.2 | Matriz eléctrica/HDL aprobada, BOM <300.000 CLP, loopback conducido y estabilidad de fase medida | Bloqueado por selección RF |
| F5 Campo | F2/F3/F4 | Condiciones y permisos documentados; pruebas progresivas con distancia independiente, Pd/Pfa e incertidumbre | Pendiente |

## Cierre del objetivo de 1 km

Antes del ensayo fijar tipo/orientación del vehículo, escenarios, velocidad, número de pasadas, distancia de referencia, criterio de asociación, Pd mínimo, Pfa máximo y sus denominadores. Registrar ensayos fallidos y blancos ausentes. Solo declarar alcance demostrado bajo las condiciones efectivamente medidas y con sus intervalos de confianza. Actualmente **no demostrado**.

## Próximas tareas

Acordar métricas cuantitativas; implementar modelo FMCW; elegir estrategia de FFT y formatos; comprobar interfaces RF; cotizar BOM completa. No hay fechas de cierre comprometidas sin resolver estas dependencias.
