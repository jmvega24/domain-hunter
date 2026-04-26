from domainhunter.models import Confidence, DomainStatus


STATUS_SCORE = {
    DomainStatus.AVAILABLE.value: 70,
    DomainStatus.PREMIUM.value: 45,
    DomainStatus.MANUAL_REVIEW.value: 25,
    DomainStatus.TAKEN.value: 5,
    DomainStatus.ERROR.value: 0,
    DomainStatus.UNKNOWN.value: 0,
}

CONFIDENCE_SCORE = {
    Confidence.HIGH.value: 15,
    Confidence.MEDIUM.value: 10,
    Confidence.LOW.value: 3,
}


def score_domain_record(record: dict[str, str]) -> dict[str, str | int]:
    domain = record["domain"]
    summary_status = record["summary_status"]
    summary_confidence = record["summary_confidence"]
    provider_statuses = record.get("provider_statuses", "")

    score = STATUS_SCORE.get(summary_status, 0)
    score += CONFIDENCE_SCORE.get(summary_confidence, 0)
    score += _provider_signal_score(provider_statuses)
    score += _name_shape_score(domain)
    score = max(0, min(score, 100))

    recommendation = _recommendation(summary_status, score)
    return {
        **record,
        "score": score,
        "recommendation": recommendation,
    }


def score_summary_records(records: list[dict[str, str]]) -> list[dict[str, str | int]]:
    scored = [score_domain_record(record) for record in records]
    return sorted(scored, key=lambda record: (-int(record["score"]), str(record["domain"])))


def shortlist_records(records: list[dict[str, str | int]], min_score: int = 30) -> list[dict[str, str | int]]:
    return [
        record
        for record in records
        if int(record["score"]) >= min_score and record["summary_status"] != DomainStatus.ERROR.value
    ]


def _provider_signal_score(provider_statuses: str) -> int:
    statuses = [
        item.split(":", 1)[1].strip()
        for item in provider_statuses.split(";")
        if ":" in item
    ]
    if not statuses:
        return 0

    available_count = statuses.count(DomainStatus.AVAILABLE.value)
    manual_review_count = statuses.count(DomainStatus.MANUAL_REVIEW.value)
    error_count = statuses.count(DomainStatus.ERROR.value)

    if available_count >= 2:
        return 10
    if available_count == 1:
        return 5
    if manual_review_count and not error_count:
        return 2
    return 0


def _name_shape_score(domain: str) -> int:
    name = domain.split(".", 1)[0]
    score = 0

    if 5 <= len(name) <= 10:
        score += 6
    elif 4 <= len(name) <= 12:
        score += 3

    if "-" not in name and any(character.isalpha() for character in name):
        score += 4

    return score


def _recommendation(summary_status: str, score: int) -> str:
    if summary_status == DomainStatus.AVAILABLE.value and score >= 70:
        return "priorizar_revision"
    if summary_status == DomainStatus.PREMIUM.value and score >= 50:
        return "revisar_precio"
    if summary_status == DomainStatus.MANUAL_REVIEW.value:
        return "revision_manual"
    if summary_status == DomainStatus.TAKEN.value:
        return "descartar_probable"
    if summary_status == DomainStatus.ERROR.value:
        return "reintentar"
    return "revision_manual"
