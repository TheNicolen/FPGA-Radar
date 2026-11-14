# Guía de contribución

1. Describir el objetivo del cambio en un Issue o en el mensaje del commit.
2. Separar propuestas de resultados verificados.
3. No subir datos de terceros sin autorización, ni credenciales ni archivos de fabricación confidenciales.
4. Documentar versión de herramientas (Vivado, Python, MATLAB, etc.).
5. Relacionar cambios de RTL con pruebas y valores esperados.
6. Los cambios que alteran arquitectura deben incorporar o actualizar un ADR.
7. Actualizar el índice de documentación, la bitácora y las tablas de requisitos cuando aplique.

## Convención de commits

`docs: ...`, `feat(fpga): ...`, `feat(jetson): ...`, `sim: ...`, `test: ...`, `fix: ...`.

## Datos y privacidad

Mantener conjuntos pequeños reproducibles en Git; para adquisiciones grandes utilizar almacenamiento externo y registrar hashes/metadatos. No publicar información personal o geolocalización precisa sin consentimiento.

## Flujo local y comprobaciones

Seguir [AGENTS.md](AGENTS.md). Revisar Git antes de cada bloque importante, mantener cambios ajenos y preparar cambios revisables. Ejecutar `python tools/check_docs.py`, `python -m unittest discover -s simulation/tests -v` y `git diff --check`; si están staged, usar también `git diff --cached --check`.

El repositorio debe permanecer privado. Antes de integrar archivos locales, inspeccionar el remoto y comparar sus archivos; no asumir que está vacío. No incluir credenciales ni usar force push.
