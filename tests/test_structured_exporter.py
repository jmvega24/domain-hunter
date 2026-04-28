import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from domainhunter.exporters.structured_exporter import (
    export_results_to_csv,
    export_results_to_json,
    export_results_to_markdown,
)
from domainhunter.models import Confidence, DomainCheckResult, DomainStatus


def _sample_results() -> list[DomainCheckResult]:
    checked_at = datetime(2026, 4, 26, tzinfo=timezone.utc)
    return [
        DomainCheckResult(
            domain="clavora.com",
            provider="godaddy",
            status=DomainStatus.MANUAL_REVIEW,
            checked_at=checked_at,
            confidence=Confidence.LOW,
            notes="captcha",
        ),
        DomainCheckResult(
            domain="clavora.com",
            provider="namecheap",
            status=DomainStatus.MANUAL_REVIEW,
            checked_at=checked_at,
            confidence=Confidence.LOW,
            notes="ambiguous",
        ),
    ]


def test_export_results_to_json_writes_results_summary_and_shortlist(tmp_path: Path) -> None:
    output = tmp_path / "results.json"

    export_results_to_json(_sample_results(), output)

    payload = json.loads(output.read_text(encoding="utf-8"))
    assert set(payload) == {"results", "summary", "shortlist"}
    assert len(payload["results"]) == 2
    assert payload["summary"][0]["domain"] == "clavora.com"
    assert payload["summary"][0]["score"] == 40
    assert payload["shortlist"][0]["recommendation"] == "revision_manual"


def test_export_results_to_csv_writes_three_files(tmp_path: Path) -> None:
    export_results_to_csv(_sample_results(), tmp_path)

    assert (tmp_path / "results.csv").exists()
    assert (tmp_path / "summary.csv").exists()
    assert (tmp_path / "shortlist.csv").exists()

    with (tmp_path / "summary.csv").open(encoding="utf-8", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))

    assert rows[0]["domain"] == "clavora.com"
    assert rows[0]["score"] == "40"


def test_export_results_to_markdown_writes_review_report(tmp_path: Path) -> None:
    output = tmp_path / "report.md"

    export_results_to_markdown(_sample_results(), output)

    report = output.read_text(encoding="utf-8")
    assert "# DomainHunter Report" in report
    assert "## Guia de revision manual" in report
    assert "revision_manual" in report
    assert "no confirma disponibilidad legal ni registral" in report
    assert "## Shortlist" in report
    assert "## Summary" in report
    assert "## Provider Results" in report
    assert "clavora.com" in report
    assert "revision_manual" in report
