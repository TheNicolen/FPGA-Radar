# Objetivos y alcance

## Problema

Estudiar la detección coherente de vehículos a larga distancia, integrando un front-end RF con procesamiento en FPGA y supervisión mediante un computador embebido.

## Objetivo general

Diseñar, implementar y caracterizar experimentalmente un prototipo de radar coherente, con núcleo de procesamiento en Nexys Video (Artix-7) y visualización en Jetson Nano, cuyo **objetivo aspiracional** sea detectar vehículos hasta 1 km.

## Objetivos específicos

1. Modelar la ecuación de radar, las señales FMCW y/o pulsos comprimidos, ruido, clutter y Doppler.
2. Definir requisitos de sensibilidad, rango dinámico, sincronización y transmisión de datos.
3. Implementar y verificar bloques de procesamiento digital en SystemVerilog.
4. Caracterizar una parabólica offset de 46 × 46 cm con un nuevo alimentador.
5. Validar primero por simulación y en banco, luego mediante pruebas radiadas autorizadas.
6. Mantener metodología, decisiones, código y resultados reproducibles en GitHub privado, sin modificar su visibilidad.

## Restricciones iniciales

- Hardware disponible declarado: reflector ~46 cm de alto y ancho. Se consideran Nexys Video y Jetson Nano como plataformas objetivo.
- Banda de interés para estudio: 2,45 GH/ 5,8 GHz, sin autorización de emisión asumida.
- Caso de uso: vehículos; RCS variable con orientación, geometría y frecuencia.

## Fuera de alcance de la primera etapa

Detección garantizada a 1 km, estimación angular precisa con una única antena fija, montaje RF de alta potencia y operación radiada no autorizada.

[Volver al índice técnico](../README.md)
