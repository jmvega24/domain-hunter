# Plan de Implementación - DomainHunter

Última actualización: 2026-04-26

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
| Fase 4 | Multi-proveedor | `backlog` | Agregar proveedor alterno y consolidar resultados por dominio. | La CLI permite elegir proveedor; resultados indican fuente y confianza. |
| Fase 5 | Scoring y shortlist | `backlog` | Ordenar candidatos por disponibilidad, precio, confianza y notas. | Export incluye score revisable y shortlist separada o filtrable. |

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

## Dependencias y Riesgos

- Playwright requiere instalación de navegador local.
- Los proveedores pueden cambiar HTML, mensajes, flujos o bloquear automatización.
- Los selectores no deben inventarse; deben validarse en ejecución antes de documentarse como activos.
- La disponibilidad reportada por un proveedor puede variar por ubicación, sesión, moneda o promociones.
- Fase 1 quedó cerrada después de ejecutar `pytest` con dependencias de desarrollo instaladas temporalmente en `/tmp/domainhunter-deps`.
- Fase 2 queda cerrada como MVP básico, pero la disponibilidad real de dominios no fue confirmada porque GoDaddy presentó validación humana.
- Fase 3 queda cerrada para robustez mínima; el riesgo activo es que GoDaddy no permita confirmar disponibilidad desde automatización.
