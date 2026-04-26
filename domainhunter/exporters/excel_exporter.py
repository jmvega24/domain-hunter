from pathlib import Path

from domainhunter.models import DomainCheckResult
from domainhunter.exporters.structured_exporter import (
    RESULT_COLUMNS,
    SUMMARY_COLUMNS,
    build_export_payload,
)


def export_results_to_excel(results: list[DomainCheckResult], output_path: Path) -> None:
    """Export normalized domain check results to an Excel workbook."""
    import pandas as pd

    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_export_payload(results)
    results_dataframe = pd.DataFrame(payload["results"], columns=RESULT_COLUMNS)
    summary_dataframe = pd.DataFrame(payload["summary"], columns=SUMMARY_COLUMNS)
    shortlist_dataframe = pd.DataFrame(payload["shortlist"], columns=SUMMARY_COLUMNS)

    with pd.ExcelWriter(output_path) as writer:
        results_dataframe.to_excel(writer, index=False, sheet_name="results")
        summary_dataframe.to_excel(writer, index=False, sheet_name="summary")
        shortlist_dataframe.to_excel(writer, index=False, sheet_name="shortlist")
