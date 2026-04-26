from domainhunter.services.scoring import score_domain_record, shortlist_records


def test_score_domain_record_scores_available_domains_highly() -> None:
    scored = score_domain_record(
        {
            "domain": "clavora.com",
            "summary_status": "available",
            "summary_confidence": "medium",
            "providers_checked": "godaddy,namecheap",
            "provider_statuses": "godaddy:manual_review; namecheap:available",
            "notes": "",
        }
    )

    assert scored["score"] == 95
    assert scored["recommendation"] == "priorizar_revision"


def test_score_domain_record_keeps_manual_review_as_manual_review() -> None:
    scored = score_domain_record(
        {
            "domain": "coreliva.com",
            "summary_status": "manual_review",
            "summary_confidence": "low",
            "providers_checked": "godaddy,namecheap",
            "provider_statuses": "godaddy:manual_review; namecheap:manual_review",
            "notes": "",
        }
    )

    assert scored["score"] == 40
    assert scored["recommendation"] == "revision_manual"


def test_shortlist_records_filters_low_score_errors() -> None:
    records = [
        {
            "domain": "clavora.com",
            "summary_status": "manual_review",
            "score": 40,
        },
        {
            "domain": "broken.com",
            "summary_status": "error",
            "score": 90,
        },
        {
            "domain": "weak.com",
            "summary_status": "taken",
            "score": 18,
        },
    ]

    assert shortlist_records(records) == [records[0]]
