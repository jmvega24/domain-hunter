from collections import defaultdict

from domainhunter.models import Confidence, DomainCheckResult, DomainStatus
from domainhunter.services.scoring import score_summary_records


STATUS_PRIORITY = {
    DomainStatus.AVAILABLE: 5,
    DomainStatus.PREMIUM: 4,
    DomainStatus.TAKEN: 3,
    DomainStatus.MANUAL_REVIEW: 2,
    DomainStatus.ERROR: 1,
    DomainStatus.UNKNOWN: 0,
}

CONFIDENCE_PRIORITY = {
    Confidence.HIGH: 3,
    Confidence.MEDIUM: 2,
    Confidence.LOW: 1,
}


def summarize_results(results: list[DomainCheckResult]) -> list[dict[str, str | int]]:
    grouped: dict[str, list[DomainCheckResult]] = defaultdict(list)
    for result in results:
        grouped[result.domain].append(result)

    summary: list[dict[str, str]] = []
    for domain, domain_results in grouped.items():
        best_result = max(
            domain_results,
            key=lambda result: (
                STATUS_PRIORITY[result.status],
                CONFIDENCE_PRIORITY[result.confidence],
            ),
        )
        summary.append(
            {
                "domain": domain,
                "summary_status": best_result.status.value,
                "summary_confidence": best_result.confidence.value,
                "providers_checked": ",".join(result.provider for result in domain_results),
                "provider_statuses": "; ".join(
                    f"{result.provider}:{result.status.value}" for result in domain_results
                ),
                "notes": " | ".join(
                    f"{result.provider}: {result.notes}"
                    for result in domain_results
                    if result.notes
                ),
            }
        )

    return score_summary_records(summary)
