from datetime import datetime, timezone

from domainhunter.models import Confidence, DomainCheckResult, DomainStatus
from domainhunter.scrapers.base import BaseScraper


class GoDaddyScraper(BaseScraper):
    provider = "godaddy"

    async def check_domain(self, domain: str) -> DomainCheckResult:
        """Placeholder scraper for Fase 2 implementation."""
        return DomainCheckResult(
            domain=domain,
            provider=self.provider,
            status=DomainStatus.MANUAL_REVIEW,
            checked_at=datetime.now(timezone.utc),
            confidence=Confidence.LOW,
            notes="Scraper pendiente de implementacion.",
        )
