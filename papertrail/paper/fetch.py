"""F1 (part 1): fetch the paper PDF.

Accepts either an arXiv URL (e.g. https://arxiv.org/abs/2106.09685 or
.../pdf/2106.09685) or a local file path, and returns raw PDF bytes
(or a local path pymupdf can open directly).
"""

import re
from pathlib import Path

import requests

_ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")


def normalize_arxiv_url(url: str) -> str:
    """Normalize an arXiv "abs" URL to its "pdf" URL equivalent."""
    match = _ARXIV_ID_RE.search(url)
    if not match:
        raise ValueError(f"Could not find an arXiv ID in URL: {url}")
    return f"https://arxiv.org/pdf/{match.group(1)}"


def fetch_paper(source: str) -> bytes:
    """Fetch a paper's PDF bytes from an arXiv URL or a local file path."""
    if "arxiv.org" in source:
        pdf_url = normalize_arxiv_url(source)
        response = requests.get(pdf_url, timeout=30)
        response.raise_for_status()
        return response.content

    local_path = Path(source)
    if not local_path.is_file():
        raise FileNotFoundError(f"No such file: {source}")
    return local_path.read_bytes()
