# 2026-11-14 — Navegación y documentación de FFT fija

- Tipo: DOCUMENTAL, PROPUESTO y ejemplo TEÓRICO
- Base remota inspeccionada: 8fd1557a189dec5a451d8357c7d8a419f45bc06e
- Estado: documentación y comprobaciones analíticas terminadas; FFT fija completa pendiente

## Cambios

Accesos S0/S1/S2 desde README; índice de simulación y subíndice FFT fija. Capítulo sobre Q1.15, twiddles Q2.16, radix-2 DIT, bit-reversal, anchos, redondeo, saturación y normalización. Cuatro esquemas SVG originales con versiones PNG. Microejemplo MATLAB de una mariposa; plan de verificación y ADR-0006 propuesto.

## Comprobaciones

Siete grupos de comprobaciones exactas en Python: mariposa contra fracciones racionales, empates positivos/negativos, saturación frente a wrap, rangos Q, bit-reversal N=8, conteos/escala y contraejemplo de saturación con entrada compleja de escala completa. [Salida verificable](../simulation/fixed-point/verification.json).

Se validó XML de los SVG, se renderizaron y revisaron las cuatro figuras y se comprobaron enlaces locales. No se ejecutó el nuevo microejemplo MATLAB ni una FFT fija completa; no se efectuó síntesis o timing. Las pruebas de S1 no se presentan como validación de esta nueva propuesta.

## Continuación

Implementar referencia completa por etapas y ROM de coeficientes, comparar contra fft(x_cuantizado)/N y después contra RTL. [Plan de pruebas](../simulation/fixed-point/PLAN.md).
