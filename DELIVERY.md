# Informe de entrega local — 2026-11-14

[Inicio](README.md)

## Estado

Copia organizada desde el paquete inicial. El 2026-11-14 se habilitó el acceso a TheNicolen/FPGA-Radar y se verificaron permisos de escritura, visibilidad privada y ausencia de ramas y archivos. El propietario autorizó cargar esta estructura en main. No se cambia la visibilidad. La versión publicada se identifica mediante el historial de commits de GitHub; la copia local se preparó inicialmente sin historial remoto.

## Comprobaciones

- Preservación: los 30 archivos originales siguen presentes; ZIP original conservado fuera de este árbol y manifiesto SHA-256 disponible.
- Seis pruebas Python aprobadas (Python 3.14.7); cálculo analítico reproducible.
- Enlaces locales Markdown comprobados con tools/check_docs.py; anclas y URLs externas fuera de alcance.
- Revisión de whitespace con Git antes de empaquetar; inventario completo a continuación.
- Sin mediciones RF, simulación FMCW completa, RTL, síntesis ni timing.
- LaTeX fuente sin compilar: pdflatex no detectado. Vivado/iverilog/verilator tampoco detectados en PATH.

## Pendientes

Simulación FMCW y cuantización; implementación RTL; selección RF y compatibilidad eléctrica/HDL; cotizaciones; caracterización de antena y validación de alcance. 1 km permanece como objetivo no demostrado.

## Archivos del paquete modificados

- [.github/ISSUE_TEMPLATE/experimento.md](.github/ISSUE_TEMPLATE/experimento.md)
- [.github/ISSUE_TEMPLATE/propuesta-tecnica.md](.github/ISSUE_TEMPLATE/propuesta-tecnica.md)
- [.gitignore](.gitignore)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [README.md](README.md)
- [ROADMAP.md](ROADMAP.md)
- [docs/01-introduccion/objetivos-y-alcance.md](docs/01-introduccion/objetivos-y-alcance.md)
- [docs/02-fundamentos/presupuesto-enlace.md](docs/02-fundamentos/presupuesto-enlace.md)
- [docs/02-fundamentos/principios-radar.md](docs/02-fundamentos/principios-radar.md)
- [docs/03-requisitos/requisitos.md](docs/03-requisitos/requisitos.md)
- [docs/04-arquitectura/arquitectura-general.md](docs/04-arquitectura/arquitectura-general.md)
- [docs/05-antenas/alimentador-cantenna.md](docs/05-antenas/alimentador-cantenna.md)
- [docs/05-antenas/reflector-directv.md](docs/05-antenas/reflector-directv.md)
- [docs/06-procesamiento/pipeline.md](docs/06-procesamiento/pipeline.md)
- [docs/07-implementacion/verificacion.md](docs/07-implementacion/verificacion.md)
- [docs/08-experimentos/protocolo.md](docs/08-experimentos/protocolo.md)
- [docs/README.md](docs/README.md)
- [docs/decisiones/ADR-0001-plataforma-digital.md](docs/decisiones/ADR-0001-plataforma-digital.md)
- [docs/decisiones/ADR-0002-seleccion-rf.md](docs/decisiones/ADR-0002-seleccion-rf.md)
- [docs/decisiones/README.md](docs/decisiones/README.md)
- [experiments/README.md](experiments/README.md)
- [fpga/README.md](fpga/README.md)
- [hardware/README.md](hardware/README.md)
- [jetson/README.md](jetson/README.md)
- [papers/README.md](papers/README.md)
- [progress/README.md](progress/README.md)
- [progress/TEMPLATE.md](progress/TEMPLATE.md)
- [references/README.md](references/README.md)
- [simulation/README.md](simulation/README.md)

## Archivos originales conservados sin cambios

- [progress/2026-11-14-inicio-documentacion.md](progress/2026-11-14-inicio-documentacion.md)

## Archivos nuevos

- [.gitattributes](.gitattributes)
- [.github/pull_request_template.md](.github/pull_request_template.md)
- [AGENTS.md](AGENTS.md)
- [docs/00-metodologia/evidencia.md](docs/00-metodologia/evidencia.md)
- [docs/00-metodologia/paquete-original.json](docs/00-metodologia/paquete-original.json)
- [docs/00-metodologia/procedencia.md](docs/00-metodologia/procedencia.md)
- [docs/06-procesamiento/interfaces.md](docs/06-procesamiento/interfaces.md)
- [docs/07-implementacion/inicio-rapido.md](docs/07-implementacion/inicio-rapido.md)
- [docs/decisiones/ADR-0003-fmcw-y-verificacion.md](docs/decisiones/ADR-0003-fmcw-y-verificacion.md)
- [docs/decisiones/ADR-0004-privacidad-y-evidencia.md](docs/decisiones/ADR-0004-privacidad-y-evidencia.md)
- [docs/decisiones/TEMPLATE.md](docs/decisiones/TEMPLATE.md)
- [experiments/TEMPLATE.md](experiments/TEMPLATE.md)
- [experiments/rf/README.md](experiments/rf/README.md)
- [fpga/constraints/README.md](fpga/constraints/README.md)
- [fpga/reports/README.md](fpga/reports/README.md)
- [fpga/rtl/README.md](fpga/rtl/README.md)
- [fpga/scripts/README.md](fpga/scripts/README.md)
- [fpga/tb/README.md](fpga/tb/README.md)
- [hardware/BOM.md](hardware/BOM.md)
- [hardware/rf/compatibilidad.md](hardware/rf/compatibilidad.md)
- [jetson/src/README.md](jetson/src/README.md)
- [jetson/tests/README.md](jetson/tests/README.md)
- [papers/ieee/figures/README.md](papers/ieee/figures/README.md)
- [papers/ieee/main.tex](papers/ieee/main.tex)
- [papers/ieee/references.bib](papers/ieee/references.bib)
- [papers/ieee/sections/01-introduccion.tex](papers/ieee/sections/01-introduccion.tex)
- [papers/ieee/sections/02-metodologia.tex](papers/ieee/sections/02-metodologia.tex)
- [papers/ieee/sections/03-resultados.tex](papers/ieee/sections/03-resultados.tex)
- [papers/ieee/sections/04-conclusiones.tex](papers/ieee/sections/04-conclusiones.tex)
- [progress/2026-11-14-organizacion-y-base-digital.md](progress/2026-11-14-organizacion-y-base-digital.md)
- [simulation/PLAN.md](simulation/PLAN.md)
- [simulation/configs/link_budget.example.json](simulation/configs/link_budget.example.json)
- [simulation/models/link_budget.py](simulation/models/link_budget.py)
- [simulation/reports/2026-11-14-calculo-enlace.md](simulation/reports/2026-11-14-calculo-enlace.md)
- [simulation/reports/README.md](simulation/reports/README.md)
- [simulation/reports/link-budget-example.json](simulation/reports/link-budget-example.json)
- [simulation/tests/test_link_budget.py](simulation/tests/test_link_budget.py)
- [simulation/vectors/README.md](simulation/vectors/README.md)
- [tools/check_docs.py](tools/check_docs.py)
- Este informe: DELIVERY.md
