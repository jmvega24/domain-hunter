# Guía Operativa Única - DomainHunter

## Propósito

DomainHunter es una herramienta CLI para validar rápidamente la disponibilidad de dominios `.com` asociados a posibles nombres de marca para una suite SaaS multi-producto.

El objetivo del agente es ayudar a construir, mantener y extender el proyecto sin perder consistencia entre código, scraping, fuentes de datos, resultados y documentación.

## Alcance del proyecto

DomainHunter debe:

- Leer una lista de dominios candidatos desde archivo.
- Consultar uno o más proveedores públicos de búsqueda de dominios mediante Playwright.
- Clasificar cada dominio con estados normalizados.
- Exportar resultados a Excel y, opcionalmente, JSON/CSV.
- Registrar errores sin detener todo el proceso.
- Facilitar iteraciones rápidas de listas de nombres.

DomainHunter no debe:

- Comprar dominios automáticamente.
- Reemplazar una revisión legal o marcaria.
- Evadir captchas, bloqueos, límites de uso o mecanismos anti-bot.
- Ejecutar scraping masivo agresivo.
- Tratar la salida del scraper como confirmación legal definitiva.

## Stack definido

- Python 3.12
- Playwright para automatización web
- Pandas + OpenPyXL para exportación de datos
- Typer para CLI
- python-dotenv para configuración
- pytest para pruebas básicas

## Fuentes canónicas

Estas fuentes deben mantenerse alineadas:

- `README.md`: visión general, instalación y uso.
- `CONTEXT.md`: estado actual del proyecto y próxima acción.
- `AGENTS.md`: reglas de trabajo para agentes IA.
- `docs/roadmap.md`: funcionalidades planificadas.
- `docs/implementation-plan.md`: fases, alcance y estado.
- `docs/slice-log.md`: bitácora de cambios relevantes.
- `docs/sources.md`: proveedores, URLs, selectores y notas de scraping.
- `data/candidates.txt`: lista de dominios a verificar.
- `data/results.xlsx`: resultados generados.

Si una fuente canónica no existe todavía, el agente debe proponer crearla antes de depender de ella.

## Reglas base de trabajo

- Trabajar por fases pequeñas y verificables.
- No abrir una nueva fase sin cerrar o dejar auditada la fase actual.
- No mezclar cambios funcionales con refactors amplios no solicitados.
- Si la documentación contradice el código, corregir la fuente canónica correspondiente.
- Si un proveedor cambia su HTML, el scraper debe fallar de forma controlada.
- Si no se puede determinar disponibilidad con confianza, usar `manual_review`.
- No inventar selectores ni comportamientos del proveedor sin validarlos en ejecución.
- Preferir una solución simple y funcional antes que una arquitectura sobredimensionada.

## Estados normalizados de dominio

Todo scraper debe devolver uno de estos estados:

| Estado | Significado |
|---|---|
| `available` | El proveedor muestra el dominio como disponible para registro estándar. |
| `taken` | El dominio aparece como no disponible o ya registrado. |
| `premium` | El dominio aparece disponible solo como premium o con precio especial. |
| `manual_review` | No se pudo determinar el estado con suficiente confianza. |
| `error` | Ocurrió un error técnico durante la consulta. |
| `unknown` | Estado inicial o no clasificado; debe evitarse en salida final. |

## Reglas para scrapers

- Usar Playwright con navegación controlada, timeouts explícitos y manejo de errores por dominio.
- Cerrar siempre browser, context y page al terminar.
- No depender de un único selector visual si puede combinarse con texto visible, URL final, badges, precio o mensajes de disponibilidad.
- Registrar evidencia mínima cuando haya error: proveedor, dominio, mensaje, timestamp y, si aplica, screenshot.
- Implementar rate limiting básico entre consultas para reducir bloqueos.
- Si aparece captcha o bloqueo, marcar el dominio como `manual_review` y continuar.
- Evitar acoplar la lógica de negocio a textos exactos que puedan cambiar fácilmente.
- Mantener los selectores documentados en `docs/sources.md`.

## Arquitectura sugerida

Estructura mínima recomendada:

```txt
domainhunter/
  __init__.py
  cli.py
  models.py
  exporters/
    excel_exporter.py
  scrapers/
    base.py
    godaddy.py
    namecheap.py
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

tests/
  test_domain_status.py
```

## Interfaz esperada de scraper

Todo scraper debe comportarse de forma equivalente a esta idea:

```python
class BaseScraper:
    async def check_domain(self, domain: str) -> DomainCheckResult:
        ...
```

El resultado debe incluir como mínimo:

- `domain`
- `provider`
- `status`
- `price`
- `currency`
- `checked_at`
- `confidence`
- `notes`
- `error_message`

## Estados narrativos de fases

Usar únicamente estos estados para fases:

- `backlog`
- `implementacion en curso`
- `implementacion lista`
- `pendiente de auditoria`
- `fase cerrada`

## Checklist antes de cerrar una tarea

Antes de cerrar una tarea o fase:

- [ ] El código ejecuta con una lista de prueba.
- [ ] Los resultados se exportan correctamente.
- [ ] Los errores de scraping no detienen todo el proceso.
- [ ] Los estados de dominio usan la taxonomía normalizada.
- [ ] `CONTEXT.md` fue actualizado.
- [ ] `docs/implementation-plan.md` o `docs/slice-log.md` fueron actualizados si aplica.
- [ ] Se propone mensaje de commit.

## Regla de cierre de fase

Una fase puede declararse `fase cerrada` solo si:

- El código funciona dentro del alcance comprometido.
- Se ejecutó contra una lista de prueba con resultados verificables.
- La documentación mínima fue actualizada.
- No hay dependencias bloqueantes sin registrar.
- Los pendientes quedan explícitos.

## Protocolo de entrega del agente

Al terminar una tarea, responder con este formato:

```md
Estado: `pendiente de auditoria` o `fase cerrada`
Alcance: fase actual
Cambios: resumen breve de lo implementado
Validación: comando ejecutado y resultado
Archivos: rutas modificadas
Pendientes: riesgos o tareas restantes
Commit sugerido: mensaje de commit propuesto
```

## Disciplina Git

- El agente no hace commit directo salvo instrucción explícita.
- El agente debe proponer mensaje de commit al cerrar una fase.
- Formato recomendado:

```txt
feat(scraper): cerrar Fase 1 - MVP de validación de dominios
```

Otros ejemplos:

```txt
docs(project): actualizar contexto operativo de DomainHunter
fix(export): manejar dominios con estado manual_review
```

## Política de tolerancia a fallos

- Si un proveedor cambia su HTML, marcar como `manual_review` o `error`, no crashear todo el lote.
- Si falla un dominio, continuar con el siguiente.
- Si falla el proveedor completo, generar salida parcial con el error registrado.
- Si aparece captcha, bloqueo o validación humana, no intentar evadirla.
- Toda excepción relevante debe quedar registrada para depuración posterior.

## Prioridad actual

La prioridad inicial es un MVP funcional:

1. Leer `data/candidates.txt`.
2. Consultar un proveedor inicial.
3. Clasificar disponibilidad con estados normalizados.
4. Exportar `data/results.xlsx`.
5. Registrar errores sin detener el proceso.
