from pathlib import Path


def read_candidate_domains(path: Path) -> list[str]:
    """Read candidate domains, ignoring blank lines and comments."""
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo de candidatos: {path}")

    domains: list[str] = []
    seen: set[str] = set()

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip().lower()
        if not line or line.startswith("#"):
            continue
        if line not in seen:
            domains.append(line)
            seen.add(line)

    return domains
