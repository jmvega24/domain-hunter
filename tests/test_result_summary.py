from datetime import datetime, timezone

from domainhunter.models import Confidence, DomainCheckResult, DomainStatus
from domainhunter.services.result_summary import summarize_results


def test_summarize_results_consolidates_by_domain() -> None:
    checked_at = datetime(2026, 4, 26, tzinfo=timezone.utc)
    results = [
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
            status=DomainStatus.AVAILABLE,
            checked_at=checked_at,
            confidence=Confidence.MEDIUM,
            notes="available",
        ),
    ]

    summary = summarize_results(results)

    assert summary == [
        {
            "domain": "clavora.com",
            "summary_status": "available",
            "summary_confidence": "medium",
            "providers_checked": "godaddy,namecheap",
            "provider_statuses": "godaddy:manual_review; namecheap:available",
            "notes": "godaddy: captcha | namecheap: available",
        }
    ]
