from pathlib import Path

from domainhunter.scrapers.base import BaseScraper
from domainhunter.scrapers.godaddy import GoDaddyScraper


def create_scraper(
    provider: str,
    timeout_ms: int = 30_000,
    headless: bool = True,
    screenshots_on_error: bool = True,
    evidence_dir: Path = Path("logs"),
) -> BaseScraper:
    normalized_provider = provider.strip().lower()

    if normalized_provider == "godaddy":
        return GoDaddyScraper(
            timeout_ms=timeout_ms,
            headless=headless,
            screenshots_on_error=screenshots_on_error,
            evidence_dir=evidence_dir,
        )

    raise ValueError(f"Proveedor no soportado: {provider}")
