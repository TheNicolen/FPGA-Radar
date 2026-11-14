# Reflector offset DirecTV disponible

**Estado: geometría parcial declarada, ganancia estimada.**

| Magnitud | Valor |
|---|---|
| Alto | Aproximadamente 46 cm |
| Ancho | Aproximadamente 46 cm |
| Profundidad | PENDIENTE |
| Posición del LNB/foco | PENDIENTE |
| Ángulo offset | PENDIENTE: no derivable solo con alto y ancho |
| Tipo | Reflector de antena de TV satelital (offset, a verificar) |

## Cálculo idealizado

Para un reflector circular equivalente de diámetro de apertura `D = 0,46 m`, eficiencia hipotética `η = 0,55`:

$$G = \eta (\pi D / \lambda)^2.$$

| Frecuencia | Ganancia teórica |
|---|---:|
| 2,45 GHz | ≈ 18,8 dBi |
| 5,8 GHz | ≈ 26,3 dBi |
| 10,5 GHz | ≈ 31,5 dBi |

Estas cifras **no** constituyen ganancias medidas. La apertura proyectada real, bloqueo, iluminación, pérdidas, geometría offset y ajuste del alimentador cambiarán el resultado.

## Trabajo pendiente

1. Fotografiar reflector de frente y perfil con regla de escala.
2. Medir profundidad vertical y horizontal; localizar geometría del soporte LNB.
3. Diseñar un soporte ajustable que no dañe la estructura original.
4. Caracterizar `S11` del alimentador (que no demuestra por sí solo buena ganancia).
5. Determinar dirección del lóbulo principal y patrón de recepción mediante una fuente conocida y pruebas pasivas.

Para pruebas radar coherentes, deberá verificarse también aislamiento TX/RX y ruido de recepción.

[Volver al índice técnico](../README.md)
