# Informes IEEE en LaTeX

[Inicio](../README.md) · [Plantilla](ieee/main.tex)

Plantilla fuente con clase IEEEtran y capítulos en `ieee/sections/`. No contiene resultados experimentales. No implica aceptación por IEEE ni cumplimiento de una convocatoria concreta.

Requiere distribución TeX con IEEEtran, babel español, amsmath y graphicx. Desde `papers/ieee`:

```console
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Bibliografía aún vacía; activar BibTeX cuando existan citas verificadas. Registrar versión y revisar el PDF visualmente antes de entregar un informe. La plantilla no ha sido compilada en este entorno: no se detectó pdflatex.
