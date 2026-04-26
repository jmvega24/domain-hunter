from pathlib import Path

from domainhunter.models import DomainCheckResult
from domainhunter.services.result_summary import summarize_results
from domainhunter.services.scoring import shortlist_records


def export_results_to_excel(results: list[DomainCheckResult], output_path: Path) -> None:
    """Export normalized domain check results to an Excel workbook."""
    import pandas as pd

    output_path.parent.mkdir(parents=True, exist_ok=True)
    records = [result.to_record() for result in results]
    columns = [
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
    results_dataframe = pd.DataFrame(records, columns=columns)
    summary_records = summarize_results(results)
    summary_columns = [
        "domain",
        "summary_status",
        "summary_confidence",
        "providers_checked",
        "provider_statuses",
        "score",
        "recommendation",
        "notes",
    ]
    summary_dataframe = pd.DataFrame(summary_records, columns=summary_columns)
    shortlist_dataframe = pd.DataFrame(
        shortlist_records(summary_records),
        columns=summary_columns,
    )

    with pd.ExcelWriter(output_path) as writer:
        results_dataframe.to_excel(writer, index=False, sheet_name="results")
        summary_dataframe.to_excel(writer, index=False, sheet_name="summary")
        shortlist_dataframe.to_excel(writer, index=False, sheet_name="shortlist")
