from domainhunter.models import DomainStatus


def test_domain_status_values_match_canonical_taxonomy() -> None:
    assert {status.value for status in DomainStatus} == {
        "available",
        "taken",
        "premium",
        "manual_review",
        "error",
        "unknown",
    }
