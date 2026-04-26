from domainhunter.models import DomainCheckResult
from domainhunter.scrapers.base import BaseScraper


class DomainCheckService:
    def __init__(self, scraper: BaseScraper) -> None:
        self._scraper = scraper

    async def check_domains(self, domains: list[str]) -> list[DomainCheckResult]:
        results: list[DomainCheckResult] = []
        for domain in domains:
            results.append(await self._scraper.check_domain(domain))
        return results
