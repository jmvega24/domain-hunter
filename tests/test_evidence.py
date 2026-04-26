import asyncio
import json
from datetime import datetime, timezone

from domainhunter.evidence import EvidenceRecorder, append_evidence_note, safe_filename
from domainhunter.models import DomainStatus


class FakePage:
    def __init__(self) -> None:
        self.screenshot_path = None

    async def screenshot(self, path, full_page: bool, timeout: int) -> None:
        self.screenshot_path = path
        path.write_bytes(b"fake-png")


def test_safe_filename_removes_unsafe_characters() -> None:
    assert safe_filename(" GoDaddy / clavora.com ") == "godaddy-clavora.com"


def test_evidence_recorder_writes_event_and_screenshot(tmp_path) -> None:
    checked_at = datetime(2026, 4, 26, tzinfo=timezone.utc)
    recorder = EvidenceRecorder(tmp_path, screenshots_enabled=True)
    page = FakePage()

    screenshot_path = asyncio.run(
        recorder.screenshot(
            page=page,
            provider="godaddy",
            domain="clavora.com",
            reason="manual_review",
            checked_at=checked_at,
        )
    )
    recorder.record_event(
        provider="godaddy",
        domain="clavora.com",
        status=DomainStatus.MANUAL_REVIEW,
        message="captcha",
        checked_at=checked_at,
        screenshot_path=screenshot_path,
    )

    assert screenshot_path is not None
    assert screenshot_path.exists()
    payload = json.loads(recorder.events_path.read_text(encoding="utf-8"))
    assert payload["provider"] == "godaddy"
    assert payload["domain"] == "clavora.com"
    assert payload["status"] == "manual_review"
    assert payload["screenshot_path"] == str(screenshot_path)


def test_append_evidence_note_keeps_original_note_without_screenshot() -> None:
    assert append_evidence_note("nota", None) == "nota"
