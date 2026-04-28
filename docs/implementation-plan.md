# Plan de Implementación - DomainHunter

Última actualización: 2026-04-28

## Estados Permitidos

- `backlog`
- `implementacion en curso`
- `implementacion lista`
- `pendiente de auditoria`
- `fase cerrada`

## Fases

| Fase | Nombre | Estado | Alcance | Criterio mínimo de cierre |
|---|---|---|---|---|
| Fase 0 | Normalización documental inicial | `implementacion lista` | Crear base documental canónica para desarrollo asistido con IA. | README, CONTEXT y documentos de `docs/` alineados; sin declarar capacidades no implementadas. |
| Fase 1 | Setup técnico | `fase cerrada` | Crear proyecto Python instalable, CLI base, carpetas esperadas y datos de ejemplo. | `python -m domainhunter --help` ejecuta; `pytest` corre al menos una prueba básica. |
| Fase 2 | MVP de validación | `fase cerrada` | Leer `data/candidates.txt`, consultar proveedor inicial, normalizar estados y exportar Excel. | Lista de prueba ejecutada; `data/results.xlsx` generado; errores por dominio no detienen el lote. |
| Fase 3 | Robustez operativa | `fase cerrada` | Agregar timeouts configurables, rate limiting, logs y evidencia mínima ante errores. | Casos de error, captcha/bloqueo y HTML ambiguo terminan en `manual_review` o `error` sin romper el lote. |
| Fase 4 | Multi-proveedor | `fase cerrada` | Agregar proveedor alterno y consolidar resultados por dominio. | La CLI permite elegir proveedor; resultados indican fuente y confianza. |
| Fase 5 | Scoring y shortlist | `fase cerrada` | Ordenar candidatos por disponibilidad, precio, confianza y notas. | Export incluye score revisable y shortlist separada o filtrable. |
| Fase 6 | Export estructurado | `fase cerrada` | Exportar JSON y CSV opcionales para iteraciones rápidas. | JSON y CSV contienen `results`, `summary` y `shortlist` equivalentes al Excel. |
| Fase 7 | Reporte de revisión | `fase cerrada` | Exportar reporte Markdown para revisión manual. | Reporte contiene shortlist, resumen, resultados por proveedor y referencias a evidencia. |
| Fase 8 | Hardening de calidad y revisión | `implementacion en curso` | Alinear documentación, ampliar pruebas de clasificadores y mejorar el reporte Markdown para revisión manual. | Documentación coherente, clasificadores cubiertos con casos conservadores y reporte más accionable sin cambiar la política de no confirmación definitiva. |

## Alcance Detallado por Fase

### Fase 0 - Normalización documental inicial

- Definir fuentes canónicas.
- Registrar estado real del repositorio.
- Crear documentación base en `docs/`.
- Registrar riesgos iniciales.

### Fase 1 - Setup técnico

- Crear `pyproject.toml`.
- Crear paquete `domainhunter`.
- Crear CLI mínima con Typer.
- Crear modelos iniciales de dominio y resultado.
- Crear `data/candidates.txt`.
- Crear pruebas básicas para estados normalizados.

Validación actual:

- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter --help`: correcto con Typer real.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt`: correcto en modo dry-run con Typer real.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m compileall domainhunter tests`: correcto.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m pytest`: correcto, 3 pruebas pasan.

### Fase 2 - MVP de validación

- Implementar lectura de candidatos.
- Implementar `BaseScraper`.
- Implementar un proveedor inicial, preferiblemente GoDaddy si se valida en ejecución.
- Exportar Excel con Pandas/OpenPyXL.
- Manejar errores por dominio.

Validación actual:

- `PYTHONPATH=/tmp/domainhunter-deps python3 -m pytest`: correcto, 7 pruebas pasan.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt --dry-run`: correcto.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt --output data/results.xlsx --timeout-ms 10000 --delay-seconds 0`: correcto.
- Resultado real del proveedor en 2026-04-26: GoDaddy mostró captcha/bloqueo; los 4 dominios quedaron en `manual_review` y el Excel fue generado.

### Fase 3 - Robustez operativa

- Agregar configuración por `.env`.
- Permitir sobrescribir configuración desde CLI.
- Registrar eventos JSONL con proveedor, dominio, estado, mensaje, timestamp, screenshot y error.
- Guardar screenshots ante `manual_review` o `error` cuando haya página disponible.
- Mantener rate limiting básico entre dominios.

Validación actual:

- `PYTHONPATH=/tmp/domainhunter-deps python3 -m pytest`: correcto, 11 pruebas pasan.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt --dry-run`: correcto.
- `PYTHONPATH=/tmp/domainhunter-deps DOMAINHUNTER_EVIDENCE_DIR=/tmp/domainhunter-evidence-test DOMAINHUNTER_TIMEOUT_MS=1000 DOMAINHUNTER_DELAY_SECONDS=0 python3 -m domainhunter check --file data/candidates.txt --dry-run`: correcto, lee configuración.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt --output data/results.xlsx --timeout-ms 10000 --delay-seconds 0 --evidence-dir logs --screenshots-on-error`: correcto.
- Resultado real del proveedor en 2026-04-26: GoDaddy mostró captcha/bloqueo; se generó `logs/events.jsonl`, 4 screenshots y `data/results.xlsx`.

### Fase 4 - Multi-proveedor

- Agregar scraper inicial para Namecheap.
- Permitir `--provider godaddy`, `--provider namecheap`, `--provider godaddy,namecheap` y `--provider all`.
- Exportar hoja `results` con filas por proveedor/dominio.
- Exportar hoja `summary` consolidada por dominio.
- Mantener evidencia por proveedor.

Validación actual:

- `PYTHONPATH=/tmp/domainhunter-deps python3 -m pytest`: correcto, 17 pruebas pasan.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt --provider all --dry-run`: correcto.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt --provider all --output data/results.xlsx --timeout-ms 15000 --delay-seconds 0 --evidence-dir logs --screenshots-on-error`: correcto.
- Resultado real del proveedor en 2026-04-26: GoDaddy y Namecheap devolvieron `manual_review`; el Excel contiene 8 filas en `results` y 4 filas en `summary`.

### Fase 5 - Scoring y shortlist

- Agregar score por dominio consolidado.
- Agregar recomendación textual por dominio.
- Exportar hoja `shortlist` filtrada y ordenada por score.
- Mantener `manual_review` cuando los proveedores no entregan evidencia suficiente.

Validación actual:

- `PYTHONPATH=/tmp/domainhunter-deps python3 -m pytest`: correcto, 20 pruebas pasan.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt --provider all --dry-run`: correcto.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt --provider all --output data/results.xlsx --timeout-ms 15000 --delay-seconds 0 --evidence-dir logs --screenshots-on-error`: correcto.
- Resultado real del proveedor en 2026-04-26: el Excel contiene hojas `results`, `summary` y `shortlist`; los 4 dominios quedaron con score `40` y recomendación `revision_manual`.

### Fase 6 - Export estructurado

- Agregar `--json-output`.
- Agregar `--csv-dir`.
- Reusar el mismo payload para Excel, JSON y CSV.
- Exportar CSV separados: `results.csv`, `summary.csv` y `shortlist.csv`.

Validación actual:

- `PYTHONPATH=/tmp/domainhunter-deps python3 -m pytest`: correcto, 23 pruebas pasan.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt --provider all --json-output data/results.json --csv-dir data/csv --dry-run`: correcto.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt --provider all --output data/results.xlsx --json-output data/results.json --csv-dir data/csv --timeout-ms 15000 --delay-seconds 0 --evidence-dir logs --screenshots-on-error`: correcto.
- Resultado real del proveedor en 2026-04-26: Excel, JSON y CSV generados; JSON contiene 8 `results`, 4 `summary` y 4 `shortlist`.

### Fase 7 - Reporte de revisión

- Agregar `--report-output`.
- Reusar el mismo payload de resultados para renderizar Markdown.
- Incluir secciones `Shortlist`, `Summary` y `Provider Results`.
- Mantener el aviso de que el reporte no confirma disponibilidad legal ni registral.

Validación actual:

- `PYTHONPATH=/tmp/domainhunter-deps python3 -m pytest`: correcto, 24 pruebas pasan.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt --provider all --json-output data/results.json --csv-dir data/csv --report-output data/report.md --dry-run`: correcto.
- `PYTHONPATH=/tmp/domainhunter-deps python3 -m domainhunter check --file data/candidates.txt --provider all --output data/results.xlsx --json-output data/results.json --csv-dir data/csv --report-output data/report.md --timeout-ms 15000 --delay-seconds 0 --evidence-dir logs --screenshots-on-error`: correcto.
- Resultado real del proveedor en 2026-04-26: `data/report.md` generado con 4 dominios en `revision_manual`.

### Fase 8 - Hardening de calidad y revisión

- Alinear README, contexto, roadmap y bitácora con el estado real del proyecto.
- Ampliar pruebas de clasificadores para `available`, `taken`, `premium`, captcha/bloqueo, ambigüedad y falsos positivos por dominio distinto.
- Mejorar el reporte Markdown para guiar revisión manual sin presentar conclusiones definitivas.
- Mantener fuera de alcance scraping agresivo, evasión anti-bot, compra automática y validación legal/marcaria.

Validación objetivo:

- `python -m compileall domainhunter tests`: correcto.
- `python -m pytest`: correcto en entorno con dependencias instaladas.
- `python -m domainhunter check --file data/candidates.txt --dry-run`: correcto.
- Reporte Markdown conserva `Shortlist`, `Summary` y `Provider Results`, y agrega guía de revisión manual.

## Dependencias y Riesgos

- Playwright requiere instalación de navegador local.
- Los proveedores pueden cambiar HTML, mensajes, flujos o bloquear automatización.
- Los selectores no deben inventarse; deben validarse en ejecución antes de documentarse como activos.
- La disponibilidad reportada por un proveedor puede variar por ubicación, sesión, moneda o promociones.
- Fase 1 quedó cerrada después de ejecutar `pytest` con dependencias de desarrollo instaladas temporalmente en `/tmp/domainhunter-deps`.
- Fase 2 queda cerrada como MVP básico, pero la disponibilidad real de dominios no fue confirmada porque GoDaddy presentó validación humana.
- Fase 3 queda cerrada para robustez mínima; el riesgo activo es que GoDaddy no permita confirmar disponibilidad desde automatización.
- Fase 4 queda cerrada para multi-proveedor; el riesgo activo es que ambos proveedores requieran revisión manual para estos candidatos.
- Fase 5 queda cerrada; el score es operativo y no reemplaza revisión marcaria ni confirmación manual de disponibilidad.
- Fase 6 queda cerrada; los archivos estructurados generados están fuera de Git.
- Fase 7 queda cerrada; el reporte Markdown es un artefacto de revisión y también queda fuera de Git.
- Fase 8 queda abierta para hardening; no debe abrir nuevos proveedores ni selectores no validados dentro de esta misma fase.
