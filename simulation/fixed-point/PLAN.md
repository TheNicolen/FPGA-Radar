# Plan de verificación de la FFT fija

[Subíndice](README.md) · [Contrato numérico](../../docs/06-procesamiento/fft-punto-fijo.md)

**[PROPUESTO]** La implementación completa y la ejecución MATLAB de la nueva referencia están pendientes. La comprobación disponible ahora se limita a una mariposa, redondeo, saturación y permutación/conteos.

## Secuencia

1. Fijar ROM de twiddles y archivo de configuración W/F, redondeo, overflow, N y schedule.
2. Implementar FFT flotante radix-2 con el mismo orden de mariposas y comparar contra `fft`.
3. Sustituir operaciones por enteros y limitar anchos en cada punto del contrato.
4. Comparar contra `fft(x_cuantizado)/N` para separar error interno de error de entrada.
5. Añadir ventanas cuantizadas, FFT Doppler y potencia; evaluar el efecto en CFAR.
6. Llevar vectores y coeficientes idénticos a testbench RTL; comparar códigos enteros exactamente.

## Casos y criterios previos

| Caso | Qué verificar | Criterio |
|---|---|---|
| Cero | Residuos/estado | Todos los códigos de salida cero |
| Impulso representable | Normalización y bins | Todos los bins iguales; incluir casos no divisibles por N |
| DC | Ganancia y escala | Pico k=0; amplitud coherente con /N |
| Tono complejo en bin ±k | Signo y orden | Pico en bin esperado; salida natural y permutaciones correctas |
| Dos tonos fuerte/débil | Error y espurias | Curva de detectabilidad antes de fijar mínimo admisible |
| Tono entre bins | Fuga espectral | No atribuir fuga a cuantización; misma ventana en referencias |
| Patrones extremos I/Q | Overflow | Flags/contadores exactos; comprobar saturación y no wrap accidental |
| Empates ±LSB/2 | Redondeo | Coincidencia exacta con regla especificada |
| N=8,16,128,512 | Generalidad | Comparación por etapa y salida |
| Stalls/reset/trama corta | Interfaz RTL | Sin pérdida/reordenamiento; invalidar trama incompleta |

Registrar error absoluto máximo, RMSE compleja, error relativo de energía cuando no sea cero, espurias, saturaciones por etapa y divergencias de bin. No exigir error relativo de fase en bins de amplitud casi cero. Los límites numéricos finales deben fijarse con necesidades de Pd/Pfa; no se inventa un umbral de aprobación universal.

## Alternativas a evaluar

Escala /2 por etapa con margen de entrada; crecimiento de ancho sin escala; block floating point; redondeo al par frente a empates alejados de cero. Comparar precisión, memoria, DSP y timing. Las reglas de una IP de AMD deben reproducirse con su modelo de referencia específico si se elige esa IP.
