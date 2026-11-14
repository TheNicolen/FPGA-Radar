# 2026-11-14 — Cálculo analítico de referencia

[Simulación](../README.md) · [Salida JSON](link-budget-example.json)

**[TEÓRICO]** Ejecutado con Python 3.14.7 y biblioteca estándar. No es simulación FMCW ni resultado experimental.

Comando desde la raíz:

```console
python simulation/models/link_budget.py --config simulation/configs/link_budget.example.json
```

Resultado: longitud de onda 0,122364 m; potencia recibida −133,373 dBm; ruido −97,975 dBm; SNR previa −35,398 dB; ganancia ideal requerida para 10 dB de SNR: 45,398 dB. Configuración completa y hash incluidos en el JSON.

La aritmética reproduce el ejemplo del paquete inicial. No demuestra que la integración sea alcanzable: faltan coherencia, duración, clutter, fuga, pérdidas de procesamiento, Pd/Pfa y validación de RF. Seis pruebas unitarias comprueban escala R^-4, RCS, pérdidas, ruido, cálculo lineal independiente y rechazo de entradas inválidas.
