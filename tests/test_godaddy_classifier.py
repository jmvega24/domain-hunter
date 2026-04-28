from domainhunter.models import Confidence, DomainStatus
from domainhunter.scrapers.godaddy import classify_godaddy_text


def test_classify_godaddy_text_marks_available_with_evidence() -> None:
    status, confidence, _ = classify_godaddy_text(
        "clavora.com is available Add to cart",
        "clavora.com",
    )

    assert status == DomainStatus.AVAILABLE
    assert confidence == Confidence.MEDIUM


def test_classify_godaddy_text_marks_taken_with_evidence() -> None:
    status, confidence, _ = classify_godaddy_text(
        "clavora.com is taken Try another domain",
        "clavora.com",
    )

    assert status == DomainStatus.TAKEN
    assert confidence == Confidence.MEDIUM


def test_classify_godaddy_text_marks_premium_with_evidence() -> None:
    status, confidence, _ = classify_godaddy_text(
        "clavora.com is a premium domain available for a special price",
        "clavora.com",
    )

    assert status == DomainStatus.PREMIUM
    assert confidence == Confidence.MEDIUM


def test_classify_godaddy_text_uses_manual_review_for_captcha_or_blocking() -> None:
    status, confidence, _ = classify_godaddy_text(
        "Verify you are human before continuing to GoDaddy",
        "clavora.com",
    )

    assert status == DomainStatus.MANUAL_REVIEW
    assert confidence == Confidence.LOW


def test_classify_godaddy_text_does_not_use_other_domain_as_evidence() -> None:
    status, confidence, _ = classify_godaddy_text(
        "kordiva.com is available Add to cart",
        "clavora.com",
    )

    assert status == DomainStatus.MANUAL_REVIEW
    assert confidence == Confidence.LOW


def test_classify_godaddy_text_uses_manual_review_when_evidence_is_ambiguous() -> None:
    status, confidence, _ = classify_godaddy_text(
        "Recommended domains and offers",
        "clavora.com",
    )

    assert status == DomainStatus.MANUAL_REVIEW
    assert confidence == Confidence.LOW
