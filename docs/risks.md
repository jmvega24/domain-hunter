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
| Namecheap no entrega evidencia textual suficiente | No se puede confirmar disponibilidad desde ese proveedor con el parser actual. | Marcar `manual_review`, conservar screenshot y revisar selectores más estables en una fase futura. |
| Evidencia local crece con el tiempo | `logs/` puede acumular screenshots pesados. | Mantener `logs/` fuera de Git y limpiar manualmente cuando ya no sea útil. |

## Riesgo Operativo Actual

El MVP multi-proveedor existe, exporta resultados y registra evidencia. GoDaddy presentó validación humana y Namecheap no entregó evidencia suficiente en la prueba real, así que la siguiente fase debe ayudar a priorizar candidatos para revisión manual.
