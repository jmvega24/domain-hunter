from dataclasses import asdict, dataclass
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

    def to_record(self) -> dict[str, str | None]:
        record = asdict(self)
        record["status"] = self.status.value
        record["confidence"] = self.confidence.value
        record["checked_at"] = self.checked_at.isoformat()
        return record
