# S2 — FFT en punto fijo

[Inicio](../../README.md) · [Simulaciones](../README.md) · [Estudio anterior: FMCW](../reports/2026-11-14-matlab-estudio-inicial.md)

**Estado: diseño propuesto y ejemplo analítico. No hay todavía FFT fija completa ni RTL validado.**

## Subíndice

1. [Capítulo: cómo funciona y cómo representarla](../../docs/06-procesamiento/fft-punto-fijo.md).
2. [Figura 1: bits, escala y rango](../../docs/06-procesamiento/figures/fft-formatos.svg).
3. [Figura 2: mariposa compleja y puntos de redondeo](../../docs/06-procesamiento/figures/fft-mariposa.svg).
4. [Figura 3: FFT de ocho puntos por etapas](../../docs/06-procesamiento/figures/fft-etapas.svg).
5. [Figura 4: anchos y escalado para 512 puntos](../../docs/06-procesamiento/figures/fft-escalado.svg).
6. [Microejemplo MATLAB de una mariposa](../matlab/demo_fixed_butterfly.m).
7. [Verificación exacta del ejemplo y redondeo](check_butterfly.py).
8. [Plan de pruebas de la futura FFT completa](PLAN.md).
9. [ADR-0006: contrato numérico inicial](../../docs/decisiones/ADR-0006-fft-punto-fijo.md).

## Recorrido recomendado

Primero entender `valor = entero / 2^F`. Después seguir una mariposa con números exactos, repetirla por etapas y estudiar qué ocurre cuando los resultados no caben. Solo entonces fijar arquitectura RTL y presupuesto de recursos.

Las figuras son esquemas explicativos, no resultados medidos ni diagramas de un circuito sintetizado. Se pueden regenerar con [generate_fft_figures.py](../../tools/generate_fft_figures.py).

## Ejecutar el microejemplo

Desde la raíz, en MATLAB:

```matlab
addpath('simulation/matlab');
resultado = demo_fixed_butterfly();
```

No requiere Fixed-Point Designer. Usa int64 para conservar productos intermedios y aplica explícitamente redondeo/saturación. **No calcula una FFT completa.** La comprobación automatizada independiente se ejecuta con `python simulation/fixed-point/check_butterfly.py`.

## Comprobaciones realizadas

[Siete comprobaciones analíticas aprobadas](verification.json), incluyendo un contraejemplo que satura a pesar del escalado /2. [Registro de avance](../../progress/2026-11-14-fft-fija-documentacion.md). No constituyen validación de una FFT completa ni ejecución MATLAB.
