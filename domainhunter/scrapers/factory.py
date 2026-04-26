from domainhunter.scrapers.base import BaseScraper
from domainhunter.scrapers.godaddy import GoDaddyScraper


def create_scraper(provider: str, timeout_ms: int = 30_000, headless: bool = True) -> BaseScraper:
    normalized_provider = provider.strip().lower()

    if normalized_provider == "godaddy":
        return GoDaddyScraper(timeout_ms=timeout_ms, headless=headless)

    raise ValueError(f"Proveedor no soportado: {provider}")
