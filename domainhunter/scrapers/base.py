from abc import ABC, abstractmethod

from domainhunter.models import DomainCheckResult


class BaseScraper(ABC):
    provider: str

    @abstractmethod
    async def check_domain(self, domain: str) -> DomainCheckResult:
        """Check a domain and return a normalized result."""
