from pathlib import Path

from typer.testing import CliRunner

from domainhunter.cli import app


def test_check_command_runs_in_dry_run_mode(tmp_path: Path) -> None:
    candidates = tmp_path / "candidates.txt"
    candidates.write_text("clavora.com\nkordiva.com\n", encoding="utf-8")

    result = CliRunner().invoke(app, ["check", "--file", str(candidates), "--dry-run"])

    assert result.exit_code == 0
    assert "Dominios cargados: 2" in result.output
    assert "Modo dry-run" in result.output
