import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from domainhunter.models import DomainStatus


def safe_filename(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_.-]+", "-", value.strip().lower())
    return normalized.strip("-") or "unknown"


class EvidenceRecorder:
    def __init__(self, base_dir: Path, screenshots_enabled: bool = True) -> None:
        self.base_dir = base_dir
        self.screenshots_enabled = screenshots_enabled

    @property
    def events_path(self) -> Path:
        return self.base_dir / "events.jsonl"

    async def screenshot(
        self,
        page: Any,
        provider: str,
        domain: str,
        reason: str,
        checked_at: datetime,
    ) -> Path | None:
        if page is None or not self.screenshots_enabled:
            return None

        screenshots_dir = self.base_dir / "screenshots"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        timestamp = checked_at.strftime("%Y%m%dT%H%M%SZ")
        filename = (
            f"{timestamp}_{safe_filename(provider)}_"
            f"{safe_filename(domain)}_{safe_filename(reason)}.png"
        )
        output_path = screenshots_dir / filename

        try:
            await page.screenshot(path=output_path, full_page=True, timeout=5_000)
        except Exception:
            return None

        return output_path

    def record_event(
        self,
        provider: str,
        domain: str,
        status: DomainStatus,
        message: str,
        checked_at: datetime,
        screenshot_path: Path | None = None,
        error_message: str | None = None,
    ) -> None:
        self.base_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "timestamp": checked_at.isoformat(),
            "provider": provider,
            "domain": domain,
            "status": status.value,
            "message": message,
            "screenshot_path": str(screenshot_path) if screenshot_path else None,
            "error_message": error_message,
        }

        with self.events_path.open("a", encoding="utf-8") as event_log:
            event_log.write(json.dumps(payload, ensure_ascii=False) + "\n")


def append_evidence_note(notes: str, screenshot_path: Path | None) -> str:
    if screenshot_path is None:
        return notes

    return f"{notes} Evidencia: {screenshot_path}"
