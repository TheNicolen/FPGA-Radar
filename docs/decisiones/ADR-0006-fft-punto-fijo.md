# ADR-0006 — Contrato numérico didáctico de FFT fija

- Fecha: 2026-11-14
- Estado: Propuesto; no arquitectura RTL aprobada

## Contexto

La referencia FMCW existente cuantiza entrada y después ejecuta FFT flotante. Se necesita explicar y especificar la aritmética interna antes de implementar.

## Propuesta

FFT forward radix-2 DIT: datos signed W16/F15, twiddles signed W18/F16, bit-reversal de entrada, salida natural y /2 por etapa. Productos ensanchados, redondeo al más cercano con empates alejados de cero en puntos definidos y saturación explícita al almacenar. Primer perfil de pruebas con módulo de entrada ≤0,5; no garantizar ausencia de overflow para cualquier entrada.

## Alternativas

FFT sin escalar y mayor ancho; block floating point; radix-4/radix-2²; IP AMD con su propia configuración y semántica; redondeo convergente. No se selecciona una arquitectura física por el solo hecho de usar una descomposición didáctica.

## Consecuencias

Reglas fáciles de seguir y ejemplo manual reproducible. Se pierde precisión al dividir por etapa; deben medir su impacto en blancos débiles. La amplitud debe compararse contra fft/N y ajustarse a la normalización de ventanas del estudio anterior. El microejemplo no valida una FFT entera ni recursos FPGA.

## Revisión

Actualizar tras el [plan de pruebas](../../simulation/fixed-point/PLAN.md), comparar error, overflow, recursos y timing. [Capítulo y figuras](../06-procesamiento/fft-punto-fijo.md).
