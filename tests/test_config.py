from pathlib import Path

from domainhunter.config import DomainHunterSettings


def test_settings_from_env_reads_domainhunter_values(monkeypatch) -> None:
    monkeypatch.setenv("DOMAINHUNTER_HEADLESS", "false")
    monkeypatch.setenv("DOMAINHUNTER_TIMEOUT_MS", "1234")
    monkeypatch.setenv("DOMAINHUNTER_DELAY_SECONDS", "0.25")
    monkeypatch.setenv("DOMAINHUNTER_SCREENSHOTS_ON_ERROR", "false")
    monkeypatch.setenv("DOMAINHUNTER_EVIDENCE_DIR", "tmp-evidence")

    settings = DomainHunterSettings.from_env()

    assert settings.headless is False
    assert settings.timeout_ms == 1234
    assert settings.delay_seconds == 0.25
    assert settings.screenshots_on_error is False
    assert settings.evidence_dir == Path("tmp-evidence")
