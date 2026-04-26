from pathlib import Path

from domainhunter.models import DomainCheckResult
from domainhunter.services.result_summary import summarize_results


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
    summary_dataframe = pd.DataFrame(
        summarize_results(results),
        columns=[
            "domain",
            "summary_status",
            "summary_confidence",
            "providers_checked",
            "provider_statuses",
            "notes",
        ],
    )

    with pd.ExcelWriter(output_path) as writer:
        results_dataframe.to_excel(writer, index=False, sheet_name="results")
        summary_dataframe.to_excel(writer, index=False, sheet_name="summary")
