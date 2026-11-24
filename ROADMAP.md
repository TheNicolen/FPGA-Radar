# Hoja de ruta verificable

[Inicio](README.md) · [Simulación](simulation/README.md) · [Base móvil](docs/05-antenas/base-movil.md) · [Bitácora](progress/README.md)

Los criterios de cierre son **[PROPUESTOS]**. Antes de cada ensayo se registrarán versión, configuración, condiciones, tamaño de muestra, umbrales y evidencia reproducible.

## 0. Simulaciones existentes

Se conserva el bloque de simulaciones y sus resultados. S0 contiene el [presupuesto de enlace](simulation/reports/2026-11-14-calculo-enlace.md). S1 contiene el [estudio FMCW ejecutado en MATLAB](simulation/reports/2026-11-14-matlab-estudio-inicial.md). S2 contiene la [propuesta de FFT fija y la verificación aritmética de una mariposa](simulation/fixed-point/README.md). La FFT fija completa, el clutter y las curvas de detección bajo ruido siguen pendientes.

## 1. Banco modular y montaje

| Hito | Prueba y evidencia de cierre | Estado |
|---|---|---|
| M1 · Ethernet Nexys Video → Jetson Nano | Enviar tramas sintéticas numeradas. Medir pérdidas, duplicados, latencia y caudal durante un intervalo acordado. Registrar la recuperación tras desconexión y reinicio. | Pendiente |
| M2 · Recepción y almacenamiento en Jetson | Reproducir un archivo conocido y verificar muestras, orden I/Q, secuencia, marca temporal y detección de tramas inválidas. Guardar captura y contadores. | Pendiente, tras M1 |
| M3 · HMI en Jetson | Mostrar estado del enlace, ángulos y origen de datos, mapa de prueba y grabación. Demostrar una sesión reproducible con datos sintéticos y desconexión. | Pendiente, viable en paralelo con M1 |
| M4 · Base móvil y apuntamiento manual | Levantar cotas, verificar fijación y bloqueo, medir topes y repetibilidad de ambos ejes y revisar la ruta del cable durante todo el recorrido. | Prototipo construido. Pendientes cotas y ensayos |
| M5 · Gabinete para Nexys Video, Jetson y monitor | Evaluar una torre de PC como gabinete. Dibujar distribución, soportes, ventilación, acceso a conectores y paso de cables. Verificar montaje y temperaturas en sesión de banco. | Pendiente |

## 2. Desarrollo técnico por bloques

| Hito | Trabajo | Prueba y evidencia de cierre |
|---|---|---|
| T1 · Justificación matemática y DSP | Derivar modelo I/Q, muestreo y FFT de rango y Doppler. Definir qué ruido o interferencia se busca reducir y comparar ventana, filtrado y umbral de detección. Derivar escalas, formatos y error en punto fijo. | Referencia reproducible con entradas idénticas antes/después. Medir SNR, sesgo, resolución y falsas alarmas. Comparar modelos flotante, fijo y RTL y registrar recursos y timing en la placa objetivo. |
| T2 · Reconocimiento de patrones | Definir clases y rasgos de la firma en rango–Doppler. Comparar una regla base y un clasificador. Ubicación inicial candidata: extraer rasgos en el sistema digital y evaluar el clasificador en Jetson antes de decidir su partición. | Separar entrenamiento y evaluación por sesión o vehículo. Reportar matriz de confusión, muestras por clase y rechazo de desconocidos. |
| T3 · Reflector y transceptor RF propio | Levantar geometría y caracterizar alimentador, apuntamiento, aislamiento Tx/Rx y coherencia. Definir la interfaz con la Nexys Video según tasas, relojes, niveles y conectores. | Ensayo conducido con cargas y atenuación, captura I/Q y verificación de coherencia, sensibilidad y espurias. Caracterizar el reflector por separado. |
| T4 · Azimut y elevación digitales | Medir cargas y recorridos. Diseñar transmisión, lectura de ángulos, referencia inicial, topes y ruta de cable. | Medir error angular, juego, repetibilidad, tiempo de estabilización y comportamiento ante límite o pérdida de referencia. |
| T5 · Alimentación del equipo | Levantar consumos de placas, monitor, RF y motores. Definir fuentes, distribución, retorno de corriente y protecciones para el gabinete. | Medir tensiones, corriente de arranque, caída al mover motores y temperaturas bajo carga. |

Para una interfaz de banda base digital, el **DAC** convierte la señal digital de **transmisión** a analógica. El **ADC** digitaliza la señal analógica de **recepción**. T3 definirá si ambos convertidores son externos o están incluidos en el transceptor y en qué punto se interconectan. La placa objetivo sigue siendo **Nexys Video**. El uso de una **Basys** como plataforma adicional de laboratorio queda por confirmar.

## 3. Integración y campaña de pruebas

| Ensayo | Evidencia esperada |
|---|---|
| Barrido | Mapa de ángulos comandados y medidos, cobertura observada, tiempo de revisita y capturas por posición. Comparar barrido por pasos y continuo cuando el control lo permita. |
| Ruido de motores | Con la misma configuración RF y ganancia, comparar motores apagados, energizados en reposo y en movimiento. Guardar I/Q y espectro, medir cambios en piso de ruido y espurias, y repetir con alimentación separada y con antena inmóvil para ayudar a distinguir acoplamiento eléctrico de vibración. |
| Identificación por firma | Pasadas repetidas con clase, trayectoria y distancia de referencia. Evaluación con sesiones reservadas e inclusión de escenas vacías. |
| Robustez | Verificar pérdida Ethernet, recuperación, deriva térmica, estabilidad del carro, flexión y torsión de los cables, y verificar lluvia/polvo solo según la protección que se construya. |
| Alcance | Incrementar distancia en ensayos de campo aplicables. Registrar orientación, velocidad, asociación, pasadas fallidas, escenas sin blancos, Pd/Pfa y sus denominadores e incertidumbre. **1 km sigue siendo un objetivo pendiente de validación.** |

El siguiente bloque de banco es **M1–M3**, con datos sintéticos. En paralelo puede completarse el levantamiento **M4**. El cierre de integración requiere revisar el gabinete, la alimentación y el RF conducido antes de la campaña de campo.
