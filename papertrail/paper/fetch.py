"""F1 (part 1): fetch the paper PDF.

Accepts either an arXiv URL (e.g. https://arxiv.org/abs/2106.09685 or
.../pdf/2106.09685) or a local file path, and returns raw PDF bytes
(or a local path pymupdf can open directly).

TODO:
    - def fetch_paper(source: str) -> bytes | str
    - Normalize arxiv "abs" URLs to "pdf" URLs before downloading
    - Handle local file paths (skip download)
    - Basic error handling: 404, malformed URL, non-arXiv source
      (v1 scope is arXiv only per PRD; other sources can raise
      NotImplementedError with a clear message for now)
"""
