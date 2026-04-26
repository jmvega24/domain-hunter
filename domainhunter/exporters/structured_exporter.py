import csv
import json
from pathlib import Path
from typing import Any

from domainhunter.models import DomainCheckResult
from domainhunter.services.result_summary import summarize_results
from domainhunter.services.scoring import shortlist_records


RESULT_COLUMNS = [
    "domain",
    "provider",
    "status",
    "price",
    "currency",
    "checked_at",
    "confidence",
    "notes",
    "error_message",
]

SUMMARY_COLUMNS = [
    "domain",
    "summary_status",
    "summary_confidence",
    "providers_checked",
    "provider_statuses",
    "score",
    "recommendation",
    "notes",
]


def build_export_payload(results: list[DomainCheckResult]) -> dict[str, list[dict[str, Any]]]:
    result_records = [result.to_record() for result in results]
    summary_records = summarize_results(results)
    return {
        "results": result_records,
        "summary": summary_records,
        "shortlist": shortlist_records(summary_records),
    }


def export_results_to_json(results: list[DomainCheckResult], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(build_export_payload(results), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def export_results_to_csv(results: list[DomainCheckResult], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = build_export_payload(results)
    _write_csv(output_dir / "results.csv", payload["results"], RESULT_COLUMNS)
    _write_csv(output_dir / "summary.csv", payload["summary"], SUMMARY_COLUMNS)
    _write_csv(output_dir / "shortlist.csv", payload["shortlist"], SUMMARY_COLUMNS)


def _write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
