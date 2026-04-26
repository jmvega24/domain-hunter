# Fuentes y Proveedores - DomainHunter

Última actualización: 2026-04-26

Este archivo documenta proveedores, URLs, selectores y observaciones de scraping. No se deben registrar selectores como válidos hasta verificarlos en ejecución.

## Proveedores Objetivo

| Proveedor | Estado | Prioridad | Nota |
|---|---|---:|---|
| GoDaddy | `fase cerrada` para MVP básico | Alta | Se consultó con Playwright el 2026-04-26. Mostró captcha/bloqueo, por lo que la clasificación correcta fue `manual_review`. |
| Namecheap | `backlog` | Media | Candidato alterno para contraste futuro. Selectores pendientes de validación. |

## GoDaddy

- URL usada: `https://www.godaddy.com/domainsearch/find?domainToCheck={domain}`
- Método actual: Playwright abre la página, lee texto visible de `body` y aplica señales conservadoras.
- Resultado observado el 2026-04-26: captcha, bloqueo o validación humana.
- Estado asignado ante ese caso: `manual_review`.
- No hay selectores específicos de disponibilidad validados todavía.
- No se intentó evadir la validación humana.

## Reglas de Documentación de Selectores

Al validar un proveedor, registrar:

- URL inicial consultada.
- Flujo de navegación.
- Selectores usados.
- Textos o señales combinadas para clasificar estado.
- Evidencia de premium, precio o moneda.
- Comportamiento ante captcha, bloqueo o timeout.
- Fecha de validación.
- Comando o script usado para validar.

## Señales Permitidas

- Texto visible de disponibilidad.
- URL final o parámetros de búsqueda.
- Badges o etiquetas de premium.
- Precio y moneda.
- Mensajes de dominio ocupado o no disponible.
- Presencia de captcha, bloqueo o validación humana.

## Política

Si la evidencia no es suficiente, el scraper debe devolver `manual_review`. Si ocurre un fallo técnico, debe devolver `error` y continuar con el siguiente dominio.
