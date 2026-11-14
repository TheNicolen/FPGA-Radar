# Inicio de trabajo reproducible

[Índice](../README.md) · [Simulación](../../simulation/README.md) · [FPGA](../../fpga/README.md)

Desde la raíz, con Python 3.10 o posterior y sin paquetes externos:

```console
python tools/check_docs.py
python -m unittest discover -s simulation/tests -v
python simulation/models/link_budget.py --config simulation/configs/link_budget.example.json
```

El último comando produce un cálculo analítico, no una simulación FMCW ni una medición. El perfil usa supuestos ilustrativos heredados del paquete inicial.

## Primera iteración matemática

1. Acordar velocidades, resolución, actualización, Pd/Pfa y condiciones de detección.
2. Ejecutar el presupuesto de enlace; barrer distancia, RCS, pérdidas y eficiencia.
3. Implementar el modelo I/Q descrito en el [plan de simulación](../../simulation/PLAN.md).
4. Comparar distancia/Doppler estimados contra verdad sintética conocida.
5. Cuantizar y exportar vectores antes de comenzar el pipeline RTL.

## Primera iteración digital

Crear generador/reproductor de muestras y testbench con backpressure. Fijar el contrato de interfaz y formatos antes de filtros/FFT. La FFT Doppler integra coherentemente entre chirps; no sumar otra ganancia por las mismas observaciones. Ver [contrato propuesto](../06-procesamiento/interfaces.md).

Vivado, simulador HDL y distribución LaTeX no están incluidos. Registrar versión y licencia disponible antes de elegir IP. No se incluye un bitstream ni restricciones listas para programar hardware.
