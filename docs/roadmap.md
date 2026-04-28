# Roadmap - DomainHunter

Última actualización: 2026-04-28

## Visión del Producto

DomainHunter debe ser una CLI pequeña y confiable para reducir listas de dominios candidatos a una shortlist revisable. Su valor está en acelerar exploración de marca, no en reemplazar compra, verificación legal ni confirmación manual final.

## Capacidades Actuales

| Capacidad | Estado | Resultado |
|---|---|---|
| Documentación base | `fase cerrada` operativamente | Otro agente puede entender propósito, estado y siguiente paso sin reconstruir contexto. |
| Setup técnico | `fase cerrada` | Proyecto Python instalable con CLI, modelos, estructura y pruebas básicas. |
| MVP de consulta | `fase cerrada` | Lista de candidatos procesada contra proveedor inicial y exportada a Excel. |
| Robustez operativa | `fase cerrada` | Manejo controlado de errores, captcha, bloqueos, timeouts, logs y screenshots. |
| Multi-proveedor | `fase cerrada` | GoDaddy y Namecheap disponibles con resultados por proveedor y resumen consolidado. |
| Scoring y shortlist | `fase cerrada` | Score, recomendación y shortlist revisable por dominio. |
| Export estructurado | `fase cerrada` | JSON y CSV opcionales con `results`, `summary` y `shortlist`. |
| Reporte Markdown | `fase cerrada` | Reporte de revisión con shortlist, resumen, resultados por proveedor y evidencia. |

## Fase Actual

### Fase 8 - Hardening de calidad y revisión

Objetivo: mejorar confiabilidad y utilidad del MVP existente sin ampliar superficie de scraping.

Líneas de trabajo:

1. Alinear documentación con capacidades reales.
2. Ampliar pruebas de clasificadores para evitar falsos positivos.
3. Mejorar el reporte Markdown como guía de revisión manual.

## Futuro Fuera del MVP

- UI web.
- Base de datos persistente.
- Compra automática.
- Integración con APIs pagas de registradores.
- Validación legal o marcaria.
- Generación automática de nombres de marca.
- Scraping intensivo o distribuido.
- Automatización para evadir mecanismos anti-bot.
- Nuevos proveedores sin validación explícita de selectores y comportamiento.
