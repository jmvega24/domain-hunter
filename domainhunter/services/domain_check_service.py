import asyncio
from datetime import datetime, timezone

from domainhunter.models import Confidence, DomainCheckResult, DomainStatus
from domainhunter.scrapers.base import BaseScraper


class DomainCheckService:
    def __init__(self, scraper: BaseScraper, delay_seconds: float = 1.5) -> None:
        self._scraper = scraper
        self._delay_seconds = delay_seconds

    async def check_domains(self, domains: list[str]) -> list[DomainCheckResult]:
        results: list[DomainCheckResult] = []
        for index, domain in enumerate(domains):
            try:
                results.append(await self._scraper.check_domain(domain))
            except Exception as exc:  # noqa: BLE001 - batch processing must continue
                results.append(
                    DomainCheckResult(
                        domain=domain,
                        provider=self._scraper.provider,
                        status=DomainStatus.ERROR,
                        checked_at=datetime.now(timezone.utc),
                        confidence=Confidence.LOW,
                        notes="Error no controlado durante la consulta.",
                        error_message=str(exc),
                    )
                )

            if index < len(domains) - 1 and self._delay_seconds > 0:
                await asyncio.sleep(self._delay_seconds)
        return results
