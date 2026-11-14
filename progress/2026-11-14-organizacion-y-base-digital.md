# 2026-11-14 — Organización y base para desarrollo digital

- Fase: F0
- Estado: preparación local verificada; integración remota pendiente
- Tipo: avance documental y cálculo TEÓRICO, sin ensayos físicos
- Versión: documental v0.2.0; historial local aún sin commit

## Inspección previa

Workspace sin checkout Git ni artefactos adjuntos. Paquete con 30 archivos de documentación; copia extraída sin `.git`. Se preservaron ZIP original y hashes. El usuario identificó TheNicolen/FPGA-Radar; la conexión GitHub devolvió 404, por lo que no se asume repositorio remoto vacío ni se sobrescribe.

## Cambios

Capítulos con navegación; política de evidencia; cuatro ADR y plantilla; hoja de ruta verificable; carpetas RTL, testbenches, restricciones, scripts, vectores, pruebas RF, Jetson e informe IEEE LaTeX. Se añadieron cálculo analítico y pruebas; se corrigió el metadato `about` en plantillas Markdown de issues y las referencias a una futura apertura pública.

## Evidencia y verificación

[Resultado analítico](../simulation/reports/2026-11-14-calculo-enlace.md). Python 3.14.7: seis pruebas aprobadas. Comprobador local de enlaces Markdown aprobado; no comprueba anclas ni disponibilidad de URLs externas. Informe completo de archivos y comprobaciones en [entrega](../DELIVERY.md).

## Limitaciones

Sin simulación FMCW completa, simulación RTL, síntesis, timing ni mediciones RF. No se detectaron Vivado, Icarus Verilog, Verilator ni pdflatex en PATH. La plantilla LaTeX está preparada como fuente, no compilada ni revisada como PDF. No hay validación a 1 km ni de compatibilidad FMCOMMS3/Nexys Video.

## Próximos pasos

Habilitar acceso al remoto e inspeccionarlo antes de integrar; acordar métricas; ejecutar el plan de simulación; definir formatos e interfaces y comenzar RTL autochecking.

## Adenda — integración autorizada el 2026-11-14

Acceso GitHub habilitado y comprobado. TheNicolen/FPGA-Radar es privado y estaba vacío, sin ramas ni archivos. Se prepara la carga de la estructura completa en main por instrucción del propietario. El registro anterior describe el estado inicial; el historial remoto permite identificar la versión cargada. No se modifican las limitaciones de validación científica.
