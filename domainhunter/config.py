from dataclasses import dataclass
from pathlib import Path


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv
    except ModuleNotFoundError:
        return

    load_dotenv()


def _getenv(name: str, default: str) -> str:
    import os

    return os.getenv(name, default)


def _get_bool(name: str, default: bool) -> bool:
    value = _getenv(name, str(default)).strip().lower()
    return value in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class DomainHunterSettings:
    headless: bool = True
    timeout_ms: int = 30_000
    delay_seconds: float = 1.5
    screenshots_on_error: bool = True
    evidence_dir: Path = Path("logs")

    @classmethod
    def from_env(cls) -> "DomainHunterSettings":
        _load_dotenv()
        return cls(
            headless=_get_bool("DOMAINHUNTER_HEADLESS", True),
            timeout_ms=int(_getenv("DOMAINHUNTER_TIMEOUT_MS", "30000")),
            delay_seconds=float(_getenv("DOMAINHUNTER_DELAY_SECONDS", "1.5")),
            screenshots_on_error=_get_bool("DOMAINHUNTER_SCREENSHOTS_ON_ERROR", True),
            evidence_dir=Path(_getenv("DOMAINHUNTER_EVIDENCE_DIR", "logs")),
        )
