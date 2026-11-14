# ADR-0002 — Selección de front-end RF

- **Fecha:** 2026-11-14
- **Estado:** Pendiente

## Contexto

Se investigan 2,45 GHz y 5,8 GHz. La primera etapa dispone de un reflector de 46 cm; el presupuesto RF es menor que $300.000 CLP.

## Candidatos

- AD-FMCOMMS3-EBZ: conector FMC pero integración y costos no validados.
- ADALM-PLUTO: facilita pruebas SDR, no conecta directamente por FMC a la Nexys Video.
- HB100: Doppler básico, no aporta rango FMCW ni cumple como transceptor final.

## Criterios antes de decidir

Disponibilidad y costo final en Chile, datos I/Q accesibles, sincronización, ancho de banda IF, latencia, esquema de integración, normativa RF y presupuesto de enlace.

[Volver al índice técnico](../README.md)
