import asyncio
from pathlib import Path
from typing import Annotated, Any

from domainhunter.config import DomainHunterSettings
from domainhunter.exporters.excel_exporter import export_results_to_excel
from domainhunter.exporters.structured_exporter import (
    export_results_to_csv,
    export_results_to_json,
)
from domainhunter.io import read_candidate_domains
from domainhunter.scrapers.factory import create_scraper, resolve_providers
from domainhunter.services.domain_check_service import DomainCheckService

try:
    import typer
except ModuleNotFoundError:  # pragma: no cover - used only before deps are installed
    typer = None


async def _run_check_async(
    file: Path,
    provider: str,
    output: Path,
    dry_run: bool,
    timeout_ms: int | None,
    delay_seconds: float | None,
    headless: bool | None,
    screenshots_on_error: bool | None,
    evidence_dir: Path | None,
    json_output: Path | None,
    csv_dir: Path | None,
) -> int:
    settings = DomainHunterSettings.from_env()
    resolved_timeout_ms = timeout_ms if timeout_ms is not None else settings.timeout_ms
    resolved_delay_seconds = delay_seconds if delay_seconds is not None else settings.delay_seconds
    resolved_headless = headless if headless is not None else settings.headless
    resolved_screenshots_on_error = (
        screenshots_on_error
        if screenshots_on_error is not None
        else settings.screenshots_on_error
    )
    resolved_evidence_dir = evidence_dir if evidence_dir is not None else settings.evidence_dir

    domains = read_candidate_domains(file)
    providers = resolve_providers(provider)

    print(f"Proveedor(es): {', '.join(providers)}")
    print(f"Entrada: {file}")
    print(f"Salida objetivo: {output}")
    if json_output is not None:
        print(f"Salida JSON: {json_output}")
    if csv_dir is not None:
        print(f"Salida CSV: {csv_dir}")
    print(f"Evidencia: {resolved_evidence_dir}")
    print(f"Dominios cargados: {len(domains)}")

    for domain in domains:
        print(f"- {domain}")

    if dry_run:
        print("Modo dry-run: no se ejecuta scraping ni exportacion.")
        return 0

    results = []
    for provider_name in providers:
        print(f"Consultando proveedor: {provider_name}")
        scraper = create_scraper(
            provider=provider_name,
            timeout_ms=resolved_timeout_ms,
            headless=resolved_headless,
            screenshots_on_error=resolved_screenshots_on_error,
            evidence_dir=resolved_evidence_dir,
        )
        service = DomainCheckService(scraper=scraper, delay_seconds=resolved_delay_seconds)
        results.extend(await service.check_domains(domains))

    export_results_to_excel(results, output)
    if json_output is not None:
        export_results_to_json(results, json_output)
    if csv_dir is not None:
        export_results_to_csv(results, csv_dir)

    print(f"Resultados exportados: {output}")
    if json_output is not None:
        print(f"JSON exportado: {json_output}")
    if csv_dir is not None:
        print(f"CSV exportado: {csv_dir}")
    return 0


def _run_check(
    file: Path,
    provider: str,
    output: Path,
    dry_run: bool,
    timeout_ms: int | None,
    delay_seconds: float | None,
    headless: bool | None,
    screenshots_on_error: bool | None,
    evidence_dir: Path | None,
    json_output: Path | None,
    csv_dir: Path | None,
) -> int:
    return asyncio.run(
        _run_check_async(
            file=file,
            provider=provider,
            output=output,
            dry_run=dry_run,
            timeout_ms=timeout_ms,
            delay_seconds=delay_seconds,
            headless=headless,
            screenshots_on_error=screenshots_on_error,
            evidence_dir=evidence_dir,
            json_output=json_output,
            csv_dir=csv_dir,
        )
    )


if typer is not None:
    app: Any = typer.Typer(
        name="domainhunter",
        help="Valida disponibilidad de dominios candidatos.",
        no_args_is_help=True,
    )

    @app.callback()
    def main() -> None:
        """Valida disponibilidad de dominios candidatos."""

    @app.command()
    def check(
        file: Annotated[
            Path,
            typer.Option("--file", "-f", help="Archivo con un dominio candidato por linea."),
        ] = Path("data/candidates.txt"),
        provider: Annotated[
            str,
            typer.Option("--provider", "-p", help="Proveedor objetivo para la consulta."),
        ] = "godaddy",
        output: Annotated[
            Path,
            typer.Option("--output", "-o", help="Archivo de salida Excel."),
        ] = Path("data/results.xlsx"),
        dry_run: Annotated[
            bool,
            typer.Option("--dry-run", help="Lee candidatos sin ejecutar scraping ni exportar."),
        ] = False,
        timeout_ms: Annotated[
            int | None,
            typer.Option("--timeout-ms", help="Timeout de navegacion por dominio."),
        ] = None,
        delay_seconds: Annotated[
            float | None,
            typer.Option("--delay-seconds", help="Pausa entre consultas para reducir bloqueos."),
        ] = None,
        headless: Annotated[
            bool | None,
            typer.Option("--headless/--headed", help="Ejecutar navegador en modo headless."),
        ] = None,
        screenshots_on_error: Annotated[
            bool | None,
            typer.Option(
                "--screenshots-on-error/--no-screenshots-on-error",
                help="Guardar screenshots ante captcha, bloqueo o error.",
            ),
        ] = None,
        evidence_dir: Annotated[
            Path | None,
            typer.Option("--evidence-dir", help="Directorio para logs y screenshots."),
        ] = None,
        json_output: Annotated[
            Path | None,
            typer.Option("--json-output", help="Archivo JSON opcional."),
        ] = None,
        csv_dir: Annotated[
            Path | None,
            typer.Option("--csv-dir", help="Directorio CSV opcional."),
        ] = None,
    ) -> None:
        """Consulta dominios y exporta resultados normalizados."""
        exit_code = _run_check(
            file=file,
            provider=provider,
            output=output,
            dry_run=dry_run,
            timeout_ms=timeout_ms,
            delay_seconds=delay_seconds,
            headless=headless,
            screenshots_on_error=screenshots_on_error,
            evidence_dir=evidence_dir,
            json_output=json_output,
            csv_dir=csv_dir,
        )
        if exit_code:
            raise typer.Exit(code=exit_code)
else:

    def app() -> None:
        """Fallback CLI para inspeccionar el repo antes de instalar dependencias."""
        import argparse
        import sys

        parser = argparse.ArgumentParser(
            prog="domainhunter",
            description="Valida disponibilidad de dominios candidatos.",
        )
        subparsers = parser.add_subparsers(dest="command")
        check_parser = subparsers.add_parser(
            "check",
            help="Consulta dominios y exporta resultados normalizados.",
        )
        check_parser.add_argument("--file", "-f", type=Path, default=Path("data/candidates.txt"))
        check_parser.add_argument("--provider", "-p", default="godaddy")
        check_parser.add_argument("--output", "-o", type=Path, default=Path("data/results.xlsx"))
        check_parser.add_argument("--dry-run", action="store_true", default=False)
        check_parser.add_argument("--timeout-ms", type=int, default=None)
        check_parser.add_argument("--delay-seconds", type=float, default=None)
        check_parser.add_argument("--headless", action="store_true", default=None)
        check_parser.add_argument("--headed", action="store_false", dest="headless")
        check_parser.add_argument("--screenshots-on-error", action="store_true", default=None)
        check_parser.add_argument(
            "--no-screenshots-on-error",
            action="store_false",
            dest="screenshots_on_error",
        )
        check_parser.add_argument("--evidence-dir", type=Path, default=None)
        check_parser.add_argument("--json-output", type=Path, default=None)
        check_parser.add_argument("--csv-dir", type=Path, default=None)

        args = parser.parse_args()
        if args.command == "check":
            raise SystemExit(
                _run_check(
                    file=args.file,
                    provider=args.provider,
                    output=args.output,
                    dry_run=args.dry_run,
                    timeout_ms=args.timeout_ms,
                    delay_seconds=args.delay_seconds,
                    headless=args.headless,
                    screenshots_on_error=args.screenshots_on_error,
                    evidence_dir=args.evidence_dir,
                    json_output=args.json_output,
                    csv_dir=args.csv_dir,
                )
            )

        parser.print_help()
        sys.exit(0)
