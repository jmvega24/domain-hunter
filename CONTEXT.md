# CONTEXT.md - DomainHunter

Última actualización: 2026-04-26

## Estado Actual

DomainHunter tiene Fase 2 cerrada para MVP básico: paquete Python, CLI, modelos, lector de candidatos, scraper GoDaddy inicial, servicio de consulta, exportador Excel, datos de ejemplo y pruebas.

Estado narrativo actual: `fase cerrada` para Fase 2. La siguiente fase recomendada es robustez operativa.

## Contexto de Negocio

La herramienta apoya la búsqueda de un dominio raíz `.com` para una suite SaaS multi-producto. El dominio elegido podría servir como marca paraguas para productos como ERP, CRM, tareas, facturación, nómina y módulos administrativos futuros.

Patrón conceptual de uso futuro:

```txt
cliente.producto.marca.com
```

Ejemplos:

```txt
acme.erp.marca.com
acme.crm.marca.com
acme.tasks.marca.com
```

## Alcance del MVP

El MVP debe permitir:

1. Leer candidatos desde `data/candidates.txt`.
2. Consultar un proveedor inicial mediante Playwright.
3. Clasificar resultados con estados normalizados.
4. Exportar `data/results.xlsx`.
5. Registrar errores sin detener el lote.
6. Marcar como `manual_review` los casos ambiguos, bloqueados o no confiables.

## Fuera de Alcance Inicial

- Compra automática de dominios.
- Revisión legal, marcaria o comercial.
- Evasión de captchas, bloqueos o límites de uso.
- Scraping masivo agresivo.
- UI web.
- Persistencia en base de datos.
- Validación multi-proveedor obligatoria.
- Scoring avanzado de marca.

## Convenciones Importantes

Estados normalizados de dominio:

| Estado | Uso |
|---|---|
| `available` | Dominio disponible para registro estándar. |
| `taken` | Dominio ocupado o no disponible. |
| `premium` | Dominio disponible como premium o con precio especial. |
| `manual_review` | Resultado ambiguo, captcha, bloqueo o falta de evidencia suficiente. |
| `error` | Error técnico durante la consulta. |
| `unknown` | Estado inicial; debe evitarse en salida final. |

Estados narrativos de fases:

- `backlog`
- `implementacion en curso`
- `implementacion lista`
- `pendiente de auditoria`
- `fase cerrada`

## Historial de Fases

| Fase | Nombre | Estado | Alcance |
|---|---|---|---|
| Fase 0 | Normalización documental inicial | `implementacion lista` | Alinear README, contexto y documentos base. |
| Fase 1 | Setup técnico | `fase cerrada` | Crear estructura Python, dependencias, CLI base, carpetas y datos de ejemplo. |
| Fase 2 | MVP de validación | `fase cerrada` | Leer candidatos, consultar proveedor inicial, clasificar y exportar Excel. |
| Fase 3 | Robustez operativa | `backlog` | Timeouts, screenshots, logs, rate limiting y manejo de captcha/bloqueo. |
| Fase 4 | Multi-proveedor | `backlog` | Agregar proveedor alterno y consolidar resultados. |
| Fase 5 | Scoring y shortlist | `backlog` | Puntuar candidatos por disponibilidad, precio, extensión y notas. |

## Próxima Acción Recomendada

Iniciar Fase 3: agregar evidencia mínima ante errores/captcha, configuración por `.env`, y endurecer el manejo de timeouts, bloqueos y logs.

## Notas Técnicas Vigentes

- Los scrapers deben usar Playwright con timeouts explícitos.
- Cada consulta de dominio debe manejar su propio error.
- Browser, context y page deben cerrarse siempre.
- Si aparece captcha o bloqueo, no evadir; registrar `manual_review`.
- Los selectores reales se documentan solo después de validarlos en ejecución.
- No declarar una fase como `fase cerrada` sin ejecución verificable.
- Fase 1 se validó con dependencias instaladas de forma temporal en `/tmp/domainhunter-deps`, porque el sistema no tiene `python3.12-venv/ensurepip`.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter --help`, `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt`, `PYTHONPATH=/tmp/domainhunter-deps python3 -m compileall domainhunter tests` y `PYTHONPATH=/tmp/domainhunter-deps python3 -m pytest` ejecutan correctamente.
- Chromium de Playwright fue instalado en `/home/jvega/.cache/ms-playwright`.
- GoDaddy mostró captcha/bloqueo en la corrida del 2026-04-26; los resultados se exportaron como `manual_review`.
- `data/results.xlsx` se genera localmente y está ignorado por Git.

## Contradicciones Detectadas

- `README.md` anterior describía scraping y exportación como capacidades pendientes. Ya existe CLI, scraper inicial y exportación Excel.
- `AGENTS.md` usaba estados con acentos, mientras la tarea actual solicita estados sin acentos. Se normaliza la documentación operativa a estados sin acentos.

## Referencias Internas

- `AGENTS.md`
- `README.md`
- `docs/implementation-plan.md`
- `docs/roadmap.md`
- `docs/slice-log.md`
- `docs/sources.md`
- `docs/risks.md`
