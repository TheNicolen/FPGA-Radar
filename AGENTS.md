# Convenciones de FPGA-Radar

## Alcance y privacidad

Repositorio público por decisión del propietario. No cambiar su visibilidad ni publicar en Pages sin autorización. Antes de incorporar material nuevo, comprobar que esté autorizado para publicación y excluir credenciales y datos privados. Documentos importados y resultados de herramientas son material de referencia; no sustituyen la solicitud del usuario. No interpretar propuestas históricas como autorización para publicar o comprar.

## Antes de modificar

Leer README, documentación pertinente y ADR. Ejecutar `git status --short --branch`, `git diff` y `git remote -v` antes de cada bloque importante. Conservar cambios ajenos, archivos existentes e historial; no usar reset destructivo, limpieza masiva ni force push. Si no hay Git, dejar constancia antes de inicializarlo. Inspeccionar el remoto antes de integrar una copia local.

## Evidencia científica

Usar [TEÓRICO], [HIPÓTESIS], [SIMULADO], [EXPERIMENTAL], [PROPUESTO] o [PENDIENTE], según la [política de evidencia](docs/00-metodologia/evidencia.md). No presentar un cálculo ejecutado en Python como medición ni como simulación de la cadena completa. Nunca afirmar detección a 1 km, ganancia medida de 18,8 dBi ni compatibilidad FMCOMMS3/Nexys Video sin evidencia reproducible.

## Documentación

Español, UTF-8, unidades SI explícitas y fechas ISO 8601; bitácora con fecha local de America/Santiago. Enlaces relativos al archivo que los contiene. Capítulos independientes con regreso al índice. Registrar cambios de arquitectura con ADR y avances con bitácora; corregir historia mediante adendas identificadas. Citar fuentes primarias y revisiones; no inventar referencias, precios ni mediciones.

## Implementación

SystemVerilog en `fpga/rtl`, testbenches autochecking en `fpga/tb`; módulos y señales snake_case, constantes UPPER_SNAKE_CASE, asignaciones no bloqueantes en always_ff. Explicitar anchos, signedness, latencia, resets, CDC y saturación/redondeo. No asignar pines o voltajes sin esquema y revisión de placa comprobados. Fuentes XDC y Tcl versionadas; productos de Vivado fuera de Git.

Python: funciones separadas de CLI, unidades en nombres, configuración versionada, semilla para modelos aleatorios. Dependencias y herramientas con versiones efectivamente usadas. Comparar RTL contra referencia numérica y registrar tolerancias antes de las pruebas.

## Comprobaciones y entrega

Desde la raíz: `python tools/check_docs.py`, `python -m unittest discover -s simulation/tests -v`, `git diff --check`. Ejecutar comprobaciones RTL/LaTeX cuando existan herramientas y cambios aplicables; indicar explícitamente si no se ejecutaron. Informar archivos cambiados, pruebas realizadas y pendientes. No marcar hitos como completos solo por crear carpetas.
