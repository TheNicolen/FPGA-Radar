# Modelos y simulaciones

[Inicio](../README.md) · [Plan FMCW](PLAN.md) · [Inicio rápido](../docs/07-implementacion/inicio-rapido.md)

- [models/link_budget.py](models/link_budget.py): cálculo analítico paramétrico de enlace, no simulador de detección.
- [configs/link_budget.example.json](configs/link_budget.example.json): hipótesis ilustrativas, no configuración RF aprobada.
- [tests/test_link_budget.py](tests/test_link_budget.py): comprobación de escalas y casos de referencia.
- [vectors](vectors/README.md): contrato de vectores compartidos con RTL.
- [reports](reports/README.md): resúmenes reproducibles de ejecuciones.

No hay simulación FMCW completa ejecutada. El cálculo usa solo la biblioteca estándar de Python; registrar `python --version`. Las futuras dependencias numéricas deberán fijarse cuando se implemente y verifique el modelo.
