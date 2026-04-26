# DomainHunter

DomainHunter es una herramienta CLI, en fase inicial, para validar disponibilidad de dominios `.com` asociados a posibles nombres de marca para una suite SaaS multi-producto.

Su propósito es acelerar el filtrado temprano de candidatos: leer una lista de dominios, consultar un proveedor público mediante Playwright, clasificar resultados con estados normalizados y exportar una hoja revisable.

## Estado Actual

Estado del proyecto al 2026-04-26: Fase 1 cerrada.

Ya existe paquete Python, `pyproject.toml`, CLI mínima, modelos base, lector de candidatos, datos de ejemplo y pruebas básicas. El scraping y la exportación Excel real quedan para Fase 2.

## Qué Hace Hoy

- Lee candidatos desde un archivo de texto.
- Expone una CLI mínima para ejecutar una revisión en modo `dry-run`.
- Normaliza la taxonomía base de estados de dominio en el modelo.
- Incluye contratos base para scraper, servicio y exportador.
- Ejecuta pruebas básicas de setup y lectura de candidatos.

## Qué Hará el MVP

- Consultar un proveedor público de búsqueda de dominios mediante Playwright.
- Clasificar cada dominio como `available`, `taken`, `premium`, `manual_review`, `error` o `unknown`.
- Exportar resultados a Excel y, más adelante, a JSON/CSV.
- Continuar el lote aunque falle una consulta individual.

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
pytest
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

1. Implementar exportador Excel real con Pandas/OpenPyXL.
2. Implementar primer scraper Playwright con manejo de errores por dominio.
3. Ejecutar una lista de prueba y documentar resultados.

## Referencias Internas

- `AGENTS.md`
- `CONTEXT.md`
- `docs/implementation-plan.md`
- `docs/roadmap.md`
- `docs/slice-log.md`
- `docs/sources.md`
- `docs/risks.md`
