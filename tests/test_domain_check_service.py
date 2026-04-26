import asyncio

from domainhunter.models import DomainCheckResult, DomainStatus
from domainhunter.scrapers.base import BaseScraper
from domainhunter.services.domain_check_service import DomainCheckService


class BrokenScraper(BaseScraper):
    provider = "broken"

    async def check_domain(self, domain: str) -> DomainCheckResult:
        raise RuntimeError(f"boom: {domain}")


def test_domain_check_service_returns_error_result_when_domain_fails() -> None:
    service = DomainCheckService(BrokenScraper(), delay_seconds=0)

    results = asyncio.run(service.check_domains(["clavora.com"]))

    assert len(results) == 1
    assert results[0].status == DomainStatus.ERROR
    assert "boom: clavora.com" in (results[0].error_message or "")
