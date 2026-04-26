# Riesgos - DomainHunter

Última actualización: 2026-04-26

## Riesgos Principales

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Cambios de HTML en proveedores | Scraper deja de clasificar correctamente. | Combinar señales, usar timeouts y devolver `manual_review` o `error`. |
| Captcha o bloqueo anti-bot | Consultas no determinables. | No evadir; registrar `manual_review` y continuar. |
| Resultados variables por sesión o ubicación | Precios/disponibilidad inconsistentes. | Registrar proveedor, fecha, notas y confianza. Confirmar manualmente finalistas. |
| Sobreconfianza en disponibilidad | Decisiones de marca incorrectas. | Documentar que no sustituye revisión legal ni confirmación de compra. |
| Dependencias no instaladas en entorno local | No se puede ejecutar `pytest` ni Typer real. | Instalar soporte de venv/pip o usar un entorno Python preparado. |
| GoDaddy muestra captcha/bloqueo | No se puede confirmar disponibilidad desde ese proveedor. | Marcar `manual_review`, registrar evidencia y evaluar proveedor alterno. |

## Riesgo Operativo Actual

El MVP básico existe y exporta resultados, pero GoDaddy presentó validación humana en la prueba real. La siguiente fase debe mejorar evidencia operativa y evaluar estabilidad del proveedor.
