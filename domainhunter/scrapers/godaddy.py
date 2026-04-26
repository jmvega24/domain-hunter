from datetime import datetime, timezone
from urllib.parse import quote_plus

from domainhunter.models import Confidence, DomainCheckResult, DomainStatus
from domainhunter.scrapers.base import BaseScraper


class GoDaddyScraper(BaseScraper):
    provider = "godaddy"

    def __init__(self, timeout_ms: int = 30_000, headless: bool = True) -> None:
        self.timeout_ms = timeout_ms
        self.headless = headless

    async def check_domain(self, domain: str) -> DomainCheckResult:
        checked_at = datetime.now(timezone.utc)

        try:
            from playwright.async_api import TimeoutError as PlaywrightTimeoutError
            from playwright.async_api import async_playwright
        except ModuleNotFoundError as exc:
            return DomainCheckResult(
                domain=domain,
                provider=self.provider,
                status=DomainStatus.ERROR,
                checked_at=checked_at,
                confidence=Confidence.LOW,
                notes="Playwright no esta instalado en el entorno actual.",
                error_message=str(exc),
            )

        browser = None
        context = None
        page = None
        url = f"https://www.godaddy.com/domainsearch/find?domainToCheck={quote_plus(domain)}"

        try:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=self.headless)
                context = await browser.new_context()
                page = await context.new_page()
                page.set_default_timeout(self.timeout_ms)

                await page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
                await page.wait_for_load_state("networkidle", timeout=self.timeout_ms)
                body_text = await page.locator("body").inner_text(timeout=self.timeout_ms)

                status, confidence, notes = classify_godaddy_text(body_text, domain)
                return DomainCheckResult(
                    domain=domain,
                    provider=self.provider,
                    status=status,
                    checked_at=checked_at,
                    confidence=confidence,
                    notes=notes,
                )
        except PlaywrightTimeoutError as exc:
            return DomainCheckResult(
                domain=domain,
                provider=self.provider,
                status=DomainStatus.ERROR,
                checked_at=checked_at,
                confidence=Confidence.LOW,
                notes="Timeout consultando GoDaddy.",
                error_message=str(exc),
            )
        except Exception as exc:  # noqa: BLE001 - debe continuar el lote
            return DomainCheckResult(
                domain=domain,
                provider=self.provider,
                status=DomainStatus.ERROR,
                checked_at=checked_at,
                confidence=Confidence.LOW,
                notes="Error tecnico consultando GoDaddy.",
                error_message=str(exc),
            )
        finally:
            if page is not None:
                try:
                    await page.close()
                except Exception:
                    pass
            if context is not None:
                try:
                    await context.close()
                except Exception:
                    pass
            if browser is not None:
                try:
                    await browser.close()
                except Exception:
                    pass


def classify_godaddy_text(text: str, domain: str) -> tuple[DomainStatus, Confidence, str]:
    normalized = " ".join(text.lower().split())
    domain_l = domain.lower()

    if any(marker in normalized for marker in ("captcha", "verify you are human", "access denied")):
        return (
            DomainStatus.MANUAL_REVIEW,
            Confidence.LOW,
            "GoDaddy mostro captcha, bloqueo o validacion humana.",
        )

    if "premium" in normalized and domain_l in normalized:
        return (
            DomainStatus.PREMIUM,
            Confidence.MEDIUM,
            "La pagina contiene senales de dominio premium.",
        )

    available_markers = (
        f"{domain_l} is available",
        f"{domain_l} está disponible",
        f"{domain_l} esta disponible",
        "domain is available",
        "is available",
    )
    if domain_l in normalized and any(marker in normalized for marker in available_markers):
        return (
            DomainStatus.AVAILABLE,
            Confidence.MEDIUM,
            "La pagina contiene senales de disponibilidad.",
        )

    taken_markers = (
        f"{domain_l} is taken",
        f"{domain_l} is unavailable",
        f"{domain_l} no está disponible",
        f"{domain_l} no esta disponible",
        "already registered",
        "is taken",
        "unavailable",
    )
    if domain_l in normalized and any(marker in normalized for marker in taken_markers):
        return (
            DomainStatus.TAKEN,
            Confidence.MEDIUM,
            "La pagina contiene senales de dominio ocupado.",
        )

    return (
        DomainStatus.MANUAL_REVIEW,
        Confidence.LOW,
        "No se encontro evidencia suficiente para clasificar el dominio.",
    )
