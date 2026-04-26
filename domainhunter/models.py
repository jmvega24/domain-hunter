from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class DomainStatus(StrEnum):
    AVAILABLE = "available"
    TAKEN = "taken"
    PREMIUM = "premium"
    MANUAL_REVIEW = "manual_review"
    ERROR = "error"
    UNKNOWN = "unknown"


class Confidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True)
class DomainCheckResult:
    domain: str
    provider: str
    status: DomainStatus
    checked_at: datetime
    confidence: Confidence = Confidence.LOW
    price: str | None = None
    currency: str | None = None
    notes: str = ""
    error_message: str | None = None
