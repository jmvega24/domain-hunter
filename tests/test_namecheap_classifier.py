from domainhunter.models import Confidence, DomainStatus
from domainhunter.scrapers.namecheap import classify_namecheap_text


def test_classify_namecheap_text_marks_available_with_evidence() -> None:
    status, confidence, _ = classify_namecheap_text(
        "clavora.com is available Add to cart",
        "clavora.com",
    )

    assert status == DomainStatus.AVAILABLE
    assert confidence == Confidence.MEDIUM


def test_classify_namecheap_text_uses_manual_review_when_evidence_is_ambiguous() -> None:
    status, confidence, _ = classify_namecheap_text(
        "Search results and recommendations",
        "clavora.com",
    )

    assert status == DomainStatus.MANUAL_REVIEW
    assert confidence == Confidence.LOW
