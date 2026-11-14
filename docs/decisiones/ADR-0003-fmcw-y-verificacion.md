# ADR-0003 — FMCW I/Q y desarrollo con datos sintéticos

- Fecha: 2026-11-14
- Estado: Aceptado como orientación inicial del proyecto; parámetros pendientes
- Base: solicitud del responsable del proyecto

## Contexto

El objetivo es procesamiento coherente en Nexys Video con RF aún sin seleccionar. El alcance de 1 km no está demostrado.

## Decisión

Comenzar con arquitectura FMCW I/Q y referencia matemática antes del RTL. Separar modelo flotante, cuantización, simulación RTL y medición física. Mantener la interfaz sintética independiente del transceptor físico.

## Alternativas

Doppler CW como ensayo educativo sin distancia; radar pulsado o SFCW como opciones de reconsideración si el estudio de factibilidad lo justifica. No implementarlas en esta etapa.

## Consecuencias

Permite verificar DSP sin comprar RF. No valida ADC, sincronismo RF, aislamiento ni alcance. La FFT Doppler realiza integración coherente entre chirps; evitar doble contabilización de ganancia.

## Revisión

Reabrir mediante nuevo ADR si presupuesto, ancho de banda, coherencia o normativa hacen inviable FMCW. Evidencia esperada: [plan de simulación](../../simulation/PLAN.md) y [contrato digital](../06-procesamiento/interfaces.md).

[Volver al índice técnico](../README.md)
