# ADR-0001 — Separación FPGA / Jetson / RF

- **Fecha:** 2026-11-14
- **Estado:** Propuesto

## Contexto

Se requiere procesamiento reproducible de muestras I/Q, control temporal y visualización. La FPGA no genera por sí misma portadoras de microondas.

## Decisión propuesta

Utilizar Nexys Video para adquisición/procesamiento digital y Jetson Nano para supervisión y visualización, dejando síntesis y recepción de microondas a un front-end especializado.

## Alternativas

Procesar todo en un SDR con CPU/GPU; usar FPGA integrada en un SDR comercial; Basys 3 con recursos más limitados.

## Consecuencias

Mayor modularidad y valor de investigación RTL, a cambio de esfuerzo de integración, sincronización y costo de hardware.

## Adenda — 2026-11-14

La solicitud actual fija Nexys Video y Jetson Nano como plataformas objetivo: decisión aceptada a nivel de arquitectura. La entrada original se conserva; esto no confirma disponibilidad física, integración ni rendimiento.

[Volver al índice técnico](../README.md)
