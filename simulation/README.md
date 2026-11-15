# Índice de simulación

[Inicio](../README.md) · [Índice técnico](../docs/README.md) · [Hoja de ruta](../ROADMAP.md)

## Ruta de lectura

| Estudio | Pregunta | Leer | Ejecutar / datos | Estado de evidencia |
|---|---|---|---|---|
| S0 | ¿Qué potencia de eco predice el modelo? | [Presupuesto de enlace](reports/2026-11-14-calculo-enlace.md) | [Python](models/link_budget.py), [configuración](configs/link_budget.example.json) | TEÓRICO, cálculo ejecutado |
| S1 | ¿Cómo influyen antena, chirps y muestreo? | [Informe con figuras](reports/2026-11-14-matlab-estudio-inicial.md) | [MATLAB](matlab/README.md), [datos](reports/matlab-inicial/summary.json) | TEÓRICO y SIMULADO; MATLAB ejecutado |
| S2 | ¿Cómo representar la FFT con bits finitos? | [Subíndice FFT fija](fixed-point/README.md), [capítulo ilustrado](../docs/06-procesamiento/fft-punto-fijo.md) | [Microejemplo MATLAB](matlab/demo_fixed_butterfly.m), [comprobación exacta](fixed-point/check_butterfly.py) | Diseño PROPUESTO y ejemplo TEÓRICO; FFT fija completa pendiente |

S1 cuantiza la entrada, pero sus FFT internas todavía son de punto flotante. S2 documenta cómo avanzar a aritmética interna fija; no declara que ya exista una FFT fija completa validada.

## Planes y recursos comunes

- [Plan FMCW](PLAN.md): casos de señal, ruido, clutter y detección.
- [Plan de verificación FFT fija](fixed-point/PLAN.md): criterios antes de RTL.
- [Vectores compartidos con RTL](vectors/README.md).
- [Informes y resultados](reports/README.md).
- [Inicio rápido](../docs/07-implementacion/inicio-rapido.md).

Fuentes/configuraciones en Git; resultados grandes regenerables en simulation/results, ignorado. Cada informe identifica herramientas, parámetros y tipo de evidencia. Los enlaces se resuelven respecto al archivo que los contiene.
