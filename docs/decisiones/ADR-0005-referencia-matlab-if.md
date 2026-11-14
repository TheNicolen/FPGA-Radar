# ADR-0005 — Referencia MATLAB desde IF dechirpeada

- Fecha: 2026-11-14
- Estado: Propuesto para estudio; no selección RF ni reloj definitivo

## Contexto

Se solicita experimentar en MATLAB con alcance, antena, frecuencia y matemática de FPGA. RF aún sin seleccionar; solo geometría aproximada del reflector disponible.

## Decisión propuesta

Separar cálculo energético de enlace de la verificación algorítmica con I/Q normalizado. Usar MATLAB base y parámetros configurables; perfil inicial 2,45 GHz, B=20 MHz, IF 2 MS/s, reloj digital candidato 100 MHz. Referencia flotante con cuantización de entrada como primer paso.

## Alternativas

Radar Toolbox/Simulink ofrecen componentes especializados, pero no son requisitos de esta primera referencia. Digitalizar el chirp completo y dechirpear en FPGA exige otro presupuesto de tasas y recursos; queda abierto junto al dechirp analógico.

## Consecuencias

Se pueden estudiar ejes y precisión sin RF. El modelo no prueba compatibilidad AD9361, capacidad FPGA, Pd/Pfa en clutter ni alcance físico. Un error de arranque/licencia MATLAB no puede sustituirse silenciosamente por una supuesta ejecución MATLAB.

## Cierre/revisión

Aceptar o revisar tras ejecutar pruebas .m, elegir front-end, definir requisitos Pd/Pfa y evaluar punto fijo/RTL. [Detalle y fuentes](../06-procesamiento/frecuencias-y-modelo-matlab.md).
