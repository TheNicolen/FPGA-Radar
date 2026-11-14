# 2026-11-14 — Laboratorio MATLAB inicial

- Fase: F0/F1, referencia matemática preliminar
- Evidencia: TEÓRICO y SIMULADO; sin mediciones RF ni FPGA
- Base remota inspeccionada: 17b231f9c048c28ee0f3f9c377214d096bb24df8
- Herramientas: MATLAB R2024b Update 9; Python 3.14.7 estándar

## Trabajo realizado

Nueve funciones MATLAB para configuración, enlace/antena, perfil de muestreo, señal I/Q, FFT 2D, cuantización, CFAR, pruebas y estudio completo. Barrido de frecuencia/eficiencia/RCS, figuras y datos reproducibles. Documentación de RF frente a Fs/reloj y ADR-0005 propuesto. Se conservaron cinco commits remotos nuevos durante el trabajo.

## Verificación

El arranque batch falló con 5202. El usuario ejecutó la línea preparada en su sesión MATLAB; se verificaron las salidas reales: ocho grupos de pruebas aprobados, figuras revisadas y seis métricas contrastadas con referencia independiente. [Informe y datos](../simulation/reports/2026-11-14-matlab-estudio-inicial.md).

## Limitaciones

No demuestra alcance físico, Fmax ni compatibilidad del front-end. FFT interna aún flotante; CFAR 1D aislado; entrada dechirpeada ideal; falta Pd en clutter. El error batch es del entorno de ejecución y no impidió ejecutar el estudio en la sesión abierta.

## Próximo paso

Diseñar dechirp/filtrado según RF y construir referencia bit-exact antes de RTL.
