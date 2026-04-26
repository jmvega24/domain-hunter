from pathlib import Path
from typing import Annotated, Any

from domainhunter.io import read_candidate_domains

try:
    import typer
except ModuleNotFoundError:  # pragma: no cover - used only before deps are installed
    typer = None


def _run_check(file: Path, provider: str, output: Path, dry_run: bool) -> int:
    domains = read_candidate_domains(file)

    print(f"Proveedor: {provider}")
    print(f"Entrada: {file}")
    print(f"Salida objetivo: {output}")
    print(f"Dominios cargados: {len(domains)}")

    for domain in domains:
        print(f"- {domain}")

    if dry_run:
        print("Modo dry-run: scraping y exportacion quedan pendientes para Fase 2.")
        return 0

    print("Scraping no implementado todavia. Ejecuta con --dry-run en Fase 1.")
    return 2


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
            typer.Option("--output", "-o", help="Archivo de salida objetivo."),
        ] = Path("data/results.xlsx"),
        dry_run: Annotated[
            bool,
            typer.Option("--dry-run", help="Lee candidatos sin ejecutar scraping."),
        ] = True,
    ) -> None:
        """Lee candidatos y muestra el plan de validacion.

        Fase 1 no ejecuta scraping ni exporta Excel; deja lista la interfaz para Fase 2.
        """
        exit_code = _run_check(file=file, provider=provider, output=output, dry_run=dry_run)
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
            help="Lee candidatos y muestra el plan de validacion.",
        )
        check_parser.add_argument("--file", "-f", type=Path, default=Path("data/candidates.txt"))
        check_parser.add_argument("--provider", "-p", default="godaddy")
        check_parser.add_argument("--output", "-o", type=Path, default=Path("data/results.xlsx"))
        check_parser.add_argument("--dry-run", action="store_true", default=True)

        args = parser.parse_args()
        if args.command == "check":
            raise SystemExit(
                _run_check(
                    file=args.file,
                    provider=args.provider,
                    output=args.output,
                    dry_run=args.dry_run,
                )
            )

        parser.print_help()
        sys.exit(0)
