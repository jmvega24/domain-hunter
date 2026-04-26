from pathlib import Path

from domainhunter.io import read_candidate_domains


def test_read_candidate_domains_ignores_comments_blank_lines_and_duplicates(tmp_path: Path) -> None:
    candidates = tmp_path / "candidates.txt"
    candidates.write_text(
        """
        # principales
        Clavora.com

        kordiva.com
        clavora.com
        """,
        encoding="utf-8",
    )

    assert read_candidate_domains(candidates) == ["clavora.com", "kordiva.com"]
