# RadarLink HMI

[Inicio](../../README.md) · [Índice Jetson](../README.md)

Ejecutar desde la raíz del repositorio, en un entorno Python que tenga PyQt5:

```bash
python jetson/src/radarlink_hmi.py --port 5005 --range 850
```

[radarlink_hmi.py](radarlink_hmi.py) contiene la interfaz. [radr_protocol.py](radr_protocol.py) decodifica detecciones, [radar_signal.py](radar_signal.py) decodifica I/Q y calcula la DFT, y [radar_signal_views.py](radar_signal_views.py) dibuja los gráficos. Los cuatro archivos deben permanecer en el mismo directorio.

El HMI reconoce detecciones RADR/RAD2 y bloques I/Q RADQ/RSC1. Para una escena sincronizada necesita cuatro detecciones RAD2 marcadas y el bloque RSC1 correspondiente. Las capturas se obtuvieron al reproducir localmente datagramas de las escenas sintéticas a través de la ruta de recepción del programa.

[Captura Principal](../figures/hmi-principal.png) · [Captura Espectro](../figures/hmi-espectro.png)
