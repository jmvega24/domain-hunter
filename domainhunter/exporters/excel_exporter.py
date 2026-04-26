from pathlib import Path

from domainhunter.models import DomainCheckResult


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
    dataframe = pd.DataFrame(records, columns=columns)
    dataframe.to_excel(output_path, index=False)
