# Alimentador tipo cantenna (guía circular)

**Estado: estudio preliminar; ningún dispositivo construido ni medido.**

Una cantenna acopla una línea coaxial de 50 Ω a una guía de ondas circular, excitada por una sonda y abierta en uno de sus extremos. Puede servir como alimentador de un reflector, pero su patrón de iluminación debe adecuarse al ángulo subtendido por éste.

## Guía circular a 2,45 GHz

La frecuencia de corte del modo dominante TE11 se aproxima mediante:

$$f_{c,TE11} = \frac{1.8412\,c}{\pi D}.$$

Para permitir TE11 a 2,45 GHz y evitar el siguiente modo TM01 idealmente el diámetro interior debe encontrarse aproximadamente entre 72 y 94 mm. Un diámetro de **85–90 mm** sería punto de partida de simulación, no una dimensión final validada.

La longitud orientativa de la sonda sería `λ0/4 ≈ 30,6 mm`; su distancia a la pared posterior requiere considerar `λg = λ0/sqrt(1 - (fc/f)^2)`. Para `D=90 mm`, `λg/4 ≈ 50,5 mm`.

## Riesgos

- Alimentación incorrecta del reflector offset y pérdidas por desbordamiento.
- Adaptación a 50 Ω inadecuada.
- Polarización, posición de foco y patrón no caracterizados.
- Confundir buena recepción Wi-Fi con desempeño de un radar coherente.

## Verificación

Simular con openEMS u otra herramienta electromagnética, medir `S11` con VNA que cubra 2,45 GHz, y comparar patrón de recepción **cantenna sola / cantenna con reflector**.

[Volver al índice técnico](../README.md)
