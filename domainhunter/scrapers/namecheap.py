from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

from domainhunter.evidence import EvidenceRecorder, append_evidence_note
from domainhunter.models import Confidence, DomainCheckResult, DomainStatus
from domainhunter.scrapers.base import BaseScraper


class NamecheapScraper(BaseScraper):
    provider = "namecheap"

    def __init__(
        self,
        timeout_ms: int = 30_000,
        headless: bool = True,
        screenshots_on_error: bool = True,
        evidence_dir: Path = Path("logs"),
    ) -> None:
        self.timeout_ms = timeout_ms
        self.headless = headless
        self.evidence = EvidenceRecorder(
            base_dir=evidence_dir,
            screenshots_enabled=screenshots_on_error,
        )

    async def check_domain(self, domain: str) -> DomainCheckResult:
        checked_at = datetime.now(timezone.utc)

        try:
            from playwright.async_api import TimeoutError as PlaywrightTimeoutError
            from playwright.async_api import async_playwright
        except ModuleNotFoundError as exc:
            notes = "Playwright no esta instalado en el entorno actual."
            self.evidence.record_event(
                provider=self.provider,
                domain=domain,
                status=DomainStatus.ERROR,
                message=notes,
                checked_at=checked_at,
                error_message=str(exc),
            )
            return DomainCheckResult(
                domain=domain,
                provider=self.provider,
                status=DomainStatus.ERROR,
                checked_at=checked_at,
                confidence=Confidence.LOW,
                notes=notes,
                error_message=str(exc),
            )

        browser = None
        context = None
        page = None
        url = f"https://www.namecheap.com/domains/registration/results/?domain={quote_plus(domain)}"

        try:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(headless=self.headless)
                context = await browser.new_context()
                page = await context.new_page()
                page.set_default_timeout(self.timeout_ms)

                await page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
                try:
                    await page.wait_for_load_state("networkidle", timeout=min(self.timeout_ms, 5_000))
                except PlaywrightTimeoutError:
                    pass
                body_text = await page.locator("body").inner_text(timeout=self.timeout_ms)

                status, confidence, notes = classify_namecheap_text(body_text, domain)
                if status in {DomainStatus.MANUAL_REVIEW, DomainStatus.ERROR}:
                    screenshot_path = await self.evidence.screenshot(
                        page=page,
                        provider=self.provider,
                        domain=domain,
                        reason=status.value,
                        checked_at=checked_at,
                    )
                    self.evidence.record_event(
                        provider=self.provider,
                        domain=domain,
                        status=status,
                        message=notes,
                        checked_at=checked_at,
                        screenshot_path=screenshot_path,
                    )
                    notes = append_evidence_note(notes, screenshot_path)

                return DomainCheckResult(
                    domain=domain,
                    provider=self.provider,
                    status=status,
                    checked_at=checked_at,
                    confidence=confidence,
                    notes=notes,
                )
        except PlaywrightTimeoutError as exc:
            notes = "Timeout consultando Namecheap."
            screenshot_path = await self.evidence.screenshot(
                page=page,
                provider=self.provider,
                domain=domain,
                reason="timeout",
                checked_at=checked_at,
            )
            self.evidence.record_event(
                provider=self.provider,
                domain=domain,
                status=DomainStatus.ERROR,
                message=notes,
                checked_at=checked_at,
                screenshot_path=screenshot_path,
                error_message=str(exc),
            )
            return DomainCheckResult(
                domain=domain,
                provider=self.provider,
                status=DomainStatus.ERROR,
                checked_at=checked_at,
                confidence=Confidence.LOW,
                notes=append_evidence_note(notes, screenshot_path),
                error_message=str(exc),
            )
        except Exception as exc:  # noqa: BLE001 - debe continuar el lote
            notes = "Error tecnico consultando Namecheap."
            screenshot_path = await self.evidence.screenshot(
                page=page,
                provider=self.provider,
                domain=domain,
                reason="error",
                checked_at=checked_at,
            )
            self.evidence.record_event(
                provider=self.provider,
                domain=domain,
                status=DomainStatus.ERROR,
                message=notes,
                checked_at=checked_at,
                screenshot_path=screenshot_path,
                error_message=str(exc),
            )
            return DomainCheckResult(
                domain=domain,
                provider=self.provider,
                status=DomainStatus.ERROR,
                checked_at=checked_at,
                confidence=Confidence.LOW,
                notes=append_evidence_note(notes, screenshot_path),
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


def classify_namecheap_text(text: str, domain: str) -> tuple[DomainStatus, Confidence, str]:
    normalized = " ".join(text.lower().split())
    domain_l = domain.lower()

    if any(
        marker in normalized
        for marker in (
            "captcha",
            "verify you are human",
            "access denied",
            "security check",
            "blocked",
        )
    ):
        return (
            DomainStatus.MANUAL_REVIEW,
            Confidence.LOW,
            "Namecheap mostro captcha, bloqueo o validacion humana.",
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
        "add to cart",
    )
    if domain_l in normalized and any(marker in normalized for marker in available_markers):
        return (
            DomainStatus.AVAILABLE,
            Confidence.MEDIUM,
            "La pagina contiene senales de disponibilidad.",
        )

    taken_markers = (
        f"{domain_l} is unavailable",
        f"{domain_l} is taken",
        f"{domain_l} no está disponible",
        f"{domain_l} no esta disponible",
        "already registered",
        "domain is taken",
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
