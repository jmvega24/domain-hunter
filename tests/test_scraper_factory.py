from domainhunter.scrapers.factory import resolve_providers


def test_resolve_providers_supports_all() -> None:
    assert resolve_providers("all") == ["godaddy", "namecheap"]


def test_resolve_providers_supports_comma_separated_values() -> None:
    assert resolve_providers("godaddy,namecheap") == ["godaddy", "namecheap"]
