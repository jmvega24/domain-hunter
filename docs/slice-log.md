# Slice Log - DomainHunter

Bitácora breve de cambios relevantes. No registra fases cerradas sin evidencia técnica verificable.

| Fecha | Slice | Estado | Notas |
|---|---|---|---|
| 2026-04-25 | Normalización documental inicial | `implementacion lista` | Se crea base documental canónica para arrancar desarrollo. No hay código funcional todavía. |
| 2026-04-25 | Fase 1 - Setup técnico | `pendiente de auditoria` | Se crea paquete Python, CLI mínima, modelos, lector de candidatos, datos de ejemplo y tests. `pytest` queda bloqueado por dependencia no instalada. |
| 2026-04-26 | Cierre Fase 1 - Setup técnico | `fase cerrada` | Se ajusta README para separar capacidades actuales de MVP pendiente, se corrige la CLI Typer para exponer el subcomando `check` y se valida Fase 1 con `pytest`. |

## Próximo Registro Esperado

Iniciar Fase 2 con exportador Excel real y primer scraper Playwright validado en ejecución.
