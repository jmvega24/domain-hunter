# DomainHunter

DomainHunter es una herramienta CLI, en fase inicial, para validar disponibilidad de dominios `.com` asociados a posibles nombres de marca para una suite SaaS multi-producto.

Su propósito es acelerar el filtrado temprano de candidatos: leer una lista de dominios, consultar un proveedor público mediante Playwright, clasificar resultados con estados normalizados y exportar una hoja revisable.

## Estado Actual

Estado del proyecto al 2026-04-26: Fase 5 cerrada.

Ya existe paquete Python, CLI, modelos base, lector de candidatos, scrapers iniciales para GoDaddy y Namecheap, servicio de consulta, exportador Excel con hojas de resultados, resumen y shortlist, datos de ejemplo, pruebas básicas, configuración por `.env` y evidencia mínima ante captcha, bloqueo o error.

## Qué Hace Hoy

- Lee candidatos desde un archivo de texto.
- Consulta GoDaddy y Namecheap mediante Playwright.
- Normaliza la taxonomía base de estados de dominio en el modelo.
- Exporta resultados a `data/results.xlsx` en tres hojas: `results`, `summary` y `shortlist`.
- Calcula score y recomendación por dominio consolidado.
- Continúa el lote aunque falle o sea ambiguo un dominio.
- Registra eventos en `logs/events.jsonl`.
- Guarda screenshots en `logs/screenshots/` cuando hay página disponible.
- Ejecuta pruebas básicas de setup, configuración, lectura, exportación, evidencia y clasificación.

## Qué Hará el MVP

- Exportar JSON/CSV más adelante.

## Qué No Hace

- No compra dominios automáticamente.
- No reemplaza revisión legal, marcaria o comercial.
- No evade captchas, bloqueos, límites de uso ni mecanismos anti-bot.
- No hace scraping masivo agresivo.
- No trata la salida del scraper como confirmación definitiva.

## Stack Tecnológico

- Python 3.12
- Playwright
- Pandas
- OpenPyXL
- Typer
- python-dotenv
- pytest

## Setup Objetivo

```bash
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
playwright install chromium
```

## Comandos Principales

```bash
python -m domainhunter check --file data/candidates.txt
python -m domainhunter check --file data/candidates.txt --provider godaddy --output data/results.xlsx
python -m domainhunter check --file data/candidates.txt --provider namecheap --output data/results.xlsx
python -m domainhunter check --file data/candidates.txt --provider all --output data/results.xlsx
python -m domainhunter check --file data/candidates.txt --dry-run
python -m domainhunter check --file data/candidates.txt --timeout-ms 10000 --delay-seconds 0 --evidence-dir logs
pytest
```

## Configuración

Copiar `.env.example` a `.env` si se quieren cambiar defaults locales:

```env
DOMAINHUNTER_HEADLESS=true
DOMAINHUNTER_TIMEOUT_MS=30000
DOMAINHUNTER_DELAY_SECONDS=1.5
DOMAINHUNTER_SCREENSHOTS_ON_ERROR=true
DOMAINHUNTER_EVIDENCE_DIR=logs
```

## Entrada Esperada

`data/candidates.txt` debe contener un dominio por línea:

```txt
# candidatos principales
clavora.com
kordiva.com
nubtiva.com
```

## Salida Esperada

Archivo principal:

```txt
data/results.xlsx
```

Columnas mínimas:

| Columna | Descripción |
|---|---|
| `domain` | Dominio consultado. |
| `provider` | Proveedor usado. |
| `status` | Estado normalizado. |
| `price` | Precio detectado, si aplica. |
| `currency` | Moneda detectada, si aplica. |
| `checked_at` | Fecha y hora de consulta. |
| `confidence` | Confianza estimada: `high`, `medium`, `low`. |
| `notes` | Observaciones relevantes. |
| `error_message` | Error técnico, si aplica. |

La hoja `summary` agrega `score` y `recommendation`. La hoja `shortlist` filtra candidatos con score suficiente para revisión.

## Estructura Esperada

```txt
domainhunter/
  __init__.py
  __main__.py
  cli.py
  models.py
  exporters/
    excel_exporter.py
  scrapers/
    base.py
    godaddy.py
  services/
    domain_check_service.py

data/
  candidates.txt
  results.xlsx

docs/
  implementation-plan.md
  roadmap.md
  slice-log.md
  sources.md
  risks.md

tests/
```

## Estados Normalizados

| Estado | Significado |
|---|---|
| `available` | Disponible para registro estándar. |
| `taken` | Ocupado o no disponible. |
| `premium` | Disponible solo como premium o con precio especial. |
| `manual_review` | Resultado ambiguo o requiere revisión humana. |
| `error` | Error técnico durante la consulta. |
| `unknown` | Estado inicial o no clasificado; debe evitarse en salida final. |

## Próximos Pasos

1. Revisar manualmente los dominios que quedan en `manual_review`.
2. Mejorar selectores específicos si se decide insistir con GoDaddy o Namecheap.
3. Agregar export JSON/CSV si se vuelve necesario para iteraciones rápidas.

## Referencias Internas

- `AGENTS.md`
- `CONTEXT.md`
- `docs/implementation-plan.md`
- `docs/roadmap.md`
- `docs/slice-log.md`
- `docs/sources.md`
- `docs/risks.md`
