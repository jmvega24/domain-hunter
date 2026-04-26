import asyncio
from pathlib import Path
from typing import Annotated, Any

from domainhunter.exporters.excel_exporter import export_results_to_excel
from domainhunter.io import read_candidate_domains
from domainhunter.scrapers.factory import create_scraper
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
    timeout_ms: int,
    delay_seconds: float,
    headless: bool,
) -> int:
    domains = read_candidate_domains(file)

    print(f"Proveedor: {provider}")
    print(f"Entrada: {file}")
    print(f"Salida objetivo: {output}")
    print(f"Dominios cargados: {len(domains)}")

    for domain in domains:
        print(f"- {domain}")

    if dry_run:
        print("Modo dry-run: no se ejecuta scraping ni exportacion.")
        return 0

    scraper = create_scraper(provider=provider, timeout_ms=timeout_ms, headless=headless)
    service = DomainCheckService(scraper=scraper, delay_seconds=delay_seconds)
    results = await service.check_domains(domains)
    export_results_to_excel(results, output)

    print(f"Resultados exportados: {output}")
    return 0


def _run_check(
    file: Path,
    provider: str,
    output: Path,
    dry_run: bool,
    timeout_ms: int,
    delay_seconds: float,
    headless: bool,
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
            int,
            typer.Option("--timeout-ms", help="Timeout de navegacion por dominio."),
        ] = 30_000,
        delay_seconds: Annotated[
            float,
            typer.Option("--delay-seconds", help="Pausa entre consultas para reducir bloqueos."),
        ] = 1.5,
        headless: Annotated[
            bool,
            typer.Option("--headless/--headed", help="Ejecutar navegador en modo headless."),
        ] = True,
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
        check_parser.add_argument("--timeout-ms", type=int, default=30_000)
        check_parser.add_argument("--delay-seconds", type=float, default=1.5)
        check_parser.add_argument("--headed", action="store_true", default=False)

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
                    headless=not args.headed,
                )
            )

        parser.print_help()
        sys.exit(0)
