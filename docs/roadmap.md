# Roadmap - DomainHunter

Última actualización: 2026-04-25

## Visión del Producto

DomainHunter debe convertirse en una CLI pequeña y confiable para reducir listas de dominios candidatos a una shortlist revisable. Su valor está en acelerar exploración de marca, no en reemplazar compra, verificación legal ni confirmación manual final.

## Hitos Principales

| Hito | Resultado esperado |
|---|---|
| Documentación base | Otro agente puede entender propósito, estado y siguiente paso sin reconstruir contexto. |
| Setup técnico | Proyecto Python instalable con CLI mínima y pruebas básicas. |
| MVP de consulta | Lista de candidatos procesada contra un proveedor inicial y exportada a Excel. |
| Robustez | Manejo controlado de errores, captcha, bloqueos, timeouts y evidencia de fallos. |
| Multi-proveedor | Comparación o confirmación básica usando más de una fuente. |
| Shortlist | Export más útil para decidir qué dominios revisar manualmente. |

## Orden Recomendado de Ejecución

1. Cerrar setup técnico.
2. Implementar modelos y taxonomía de estados.
3. Implementar lectura de candidatos.
4. Implementar exportador Excel.
5. Validar un proveedor inicial con Playwright.
6. Integrar scraper al servicio de chequeo.
7. Ejecutar lista corta de prueba.
8. Documentar selectores y resultados observados.
9. Añadir tolerancia a errores y evidencia mínima.
10. Evaluar segundo proveedor.

## Futuro Fuera del MVP

- UI web.
- Base de datos persistente.
- Compra automática.
- Integración con APIs pagas de registradores.
- Validación legal o marcaria.
- Generación automática de nombres de marca.
- Scraping intensivo o distribuido.
- Automatización para evadir mecanismos anti-bot.
