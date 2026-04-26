from pathlib import Path

from domainhunter.scrapers.base import BaseScraper
from domainhunter.scrapers.godaddy import GoDaddyScraper
from domainhunter.scrapers.namecheap import NamecheapScraper


SUPPORTED_PROVIDERS = ("godaddy", "namecheap")


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
    if normalized_provider == "namecheap":
        return NamecheapScraper(
            timeout_ms=timeout_ms,
            headless=headless,
            screenshots_on_error=screenshots_on_error,
            evidence_dir=evidence_dir,
        )

    raise ValueError(f"Proveedor no soportado: {provider}")


def resolve_providers(provider: str) -> list[str]:
    normalized_provider = provider.strip().lower()
    if normalized_provider == "all":
        return list(SUPPORTED_PROVIDERS)

    providers = [item.strip().lower() for item in normalized_provider.split(",") if item.strip()]
    unsupported = [item for item in providers if item not in SUPPORTED_PROVIDERS]
    if unsupported:
        raise ValueError(f"Proveedor no soportado: {', '.join(unsupported)}")

    return providers
