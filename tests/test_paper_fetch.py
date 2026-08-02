"""Tests for papertrail.paper.fetch."""

from pathlib import Path

from papertrail.paper.fetch import fetch_paper, normalize_arxiv_url


def test_fetch_paper_reads_local_file_bytes(tmp_path):
    pdf_path = tmp_path / "paper.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 fake content")

    result = fetch_paper(str(pdf_path))

    assert result == b"%PDF-1.4 fake content"


def test_fetch_paper_missing_local_file_raises():
    import pytest

    with pytest.raises(FileNotFoundError):
        fetch_paper("does_not_exist.pdf")


def test_normalize_arxiv_abs_url_to_pdf_url():
    assert (
        normalize_arxiv_url("https://arxiv.org/abs/2106.09685")
        == "https://arxiv.org/pdf/2106.09685"
    )


def test_normalize_arxiv_pdf_url_stays_pdf_url():
    assert (
        normalize_arxiv_url("https://arxiv.org/pdf/2106.09685")
        == "https://arxiv.org/pdf/2106.09685"
    )


def test_normalize_arxiv_url_strips_version_suffix():
    assert (
        normalize_arxiv_url("https://arxiv.org/abs/2106.09685v2")
        == "https://arxiv.org/pdf/2106.09685"
    )


def test_normalize_non_arxiv_url_raises():
    import pytest

    with pytest.raises(ValueError):
        normalize_arxiv_url("https://example.com/paper.pdf")
