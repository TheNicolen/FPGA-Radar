# Evidencia y trazabilidad

[Índice técnico](../README.md) · [Inicio](../../README.md)

| Etiqueta | Significado | Evidencia mínima |
|---|---|---|
| [TEÓRICO] | Resultado analítico bajo un modelo | Ecuación, unidades, supuestos, cálculo reproducible |
| [HIPÓTESIS] | Supuesto aún no contrastado | Justificación y ensayo que lo podría refutar |
| [SIMULADO] | Resultado de una simulación ejecutada | Código, configuración, semilla, versión y salidas |
| [EXPERIMENTAL] | Medición física efectivamente realizada | Datos crudos, instrumentos/calibración, condiciones e incertidumbre |
| [PROPUESTO] | Diseño o criterio por aprobar | Alternativas, responsable y ADR si corresponde |
| [PENDIENTE] | Sin resolver o sin ejecutar | Próximo paso y criterio de cierre |

Las etiquetas históricas [ESTIMADO] y [MEDIDO] se interpretan respectivamente como cálculo/supuesto por desglosar y medición que exige respaldo. [SIMULADO] no describe simplemente un plan.

Cada resultado debe enlazar requisito → configuración y commit → ejecución → datos con SHA-256 → análisis → conclusión. Un hash certifica identidad del archivo, no veracidad de la medición. Usar null o PENDIENTE para datos desconocidos; nunca cero como sustituto de una medición ausente.

Estado inicial: no hay mediciones RF, detecciones de vehículos ni validación FPGA registradas. 1 km es un objetivo; 18,8 dBi es un cálculo idealizado con eficiencia hipotética. La disponibilidad física de FPGA/Jetson debe confirmarse.
