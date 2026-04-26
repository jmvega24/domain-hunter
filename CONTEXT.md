# CONTEXT.md - DomainHunter

Última actualización: 2026-04-26

## Estado Actual

DomainHunter tiene Fase 5 cerrada: paquete Python, CLI, modelos, lector de candidatos, scrapers iniciales para GoDaddy y Namecheap, servicio de consulta, exportador Excel con hojas `results`, `summary` y `shortlist`, datos de ejemplo, pruebas, configuración por `.env` y evidencia mínima ante captcha, bloqueo o error.

Estado narrativo actual: `fase cerrada` para Fase 5. La siguiente acción recomendada es revisión manual de candidatos o una fase nueva de export JSON/CSV.

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
| Fase 3 | Robustez operativa | `fase cerrada` | Timeouts, screenshots, logs, rate limiting y manejo de captcha/bloqueo. |
| Fase 4 | Multi-proveedor | `fase cerrada` | Agregar proveedor alterno y consolidar resultados. |
| Fase 5 | Scoring y shortlist | `fase cerrada` | Puntuar candidatos por disponibilidad, precio, extensión y notas. |

## Próxima Acción Recomendada

Revisar manualmente la hoja `shortlist` y los screenshots asociados. Si se necesita seguir automatizando, abrir una fase nueva para export JSON/CSV o selectores específicos por proveedor.

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
- Fase 3 genera `logs/events.jsonl` con proveedor, dominio, estado, mensaje, timestamp, screenshot y error si aplica.
- Fase 3 guarda screenshots en `logs/screenshots/` cuando Playwright logra abrir una página.
- `.env.example` documenta `DOMAINHUNTER_HEADLESS`, `DOMAINHUNTER_TIMEOUT_MS`, `DOMAINHUNTER_DELAY_SECONDS`, `DOMAINHUNTER_SCREENSHOTS_ON_ERROR` y `DOMAINHUNTER_EVIDENCE_DIR`.
- `--provider all` ejecuta `godaddy` y `namecheap` en secuencia.
- El Excel tiene hoja `results` con una fila por proveedor/dominio y hoja `summary` consolidada por dominio.
- Corrida real del 2026-04-26: ambos proveedores terminaron en `manual_review`; GoDaddy mostró validación humana y Namecheap no entregó evidencia suficiente en el texto visible.
- Fase 5 agrega `score` y `recommendation` a `summary`, además de una hoja `shortlist`.
- Corrida real del 2026-04-26: los 4 dominios quedaron con score `40` y recomendación `revision_manual`.

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
