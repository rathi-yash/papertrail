"""F1 (part 2): extract text and isolate relevant sections from the PDF.

Uses pymupdf (fitz) for raw text extraction, then isolates the sections
that matter for reproduction via section-header heuristics: lines that
look like all-caps headers (e.g. "HYPERPARAMETERS USED IN EXPERIMENTS",
"EXPERIMENTAL SETUP") split the document into sections, each mapped to
a canonical key if its heading matches a known keyword.
"""

import re

import fitz

_HEADER_RE = re.compile(r"^[A-Z][A-Z0-9][A-Z0-9 ,\-]{2,60}$")

# canonical section key -> keywords that identify a heading as that section
_SECTION_KEYWORDS = {
    "hyperparameters": ["hyperparameter"],
    "experimental_setup": ["experimental setup", "implementation detail"],
    "dataset": ["dataset"],
    "hardware": ["hardware"],
}


def extract_full_text(pdf_source: str) -> str:
    """Extract raw text from a PDF file path."""
    doc = fitz.open(pdf_source)
    try:
        return "".join(page.get_text() for page in doc)
    finally:
        doc.close()


def isolate_relevant_sections(full_text: str) -> dict[str, str]:
    """Split full_text into sections keyed by canonical section name.

    Uses header-line heuristics (all-caps short lines) to find section
    boundaries, then maps each heading to a canonical key if it matches
    known keywords (e.g. "HYPERPARAMETERS USED IN EXPERIMENTS" ->
    "hyperparameters").
    """
    lines = full_text.split("\n")

    headings: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # require multi-word headings to avoid false positives from
        # single-token subsection labels / model names (e.g. "ROBERTA")
        if _HEADER_RE.match(stripped) and " " in stripped:
            headings.append((i, stripped))

    sections: dict[str, str] = {}
    for idx, (line_no, heading) in enumerate(headings):
        canonical = _match_canonical_key(heading)
        if canonical is None:
            continue
        end = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        body = "\n".join(lines[line_no + 1 : end]).strip()
        if canonical in sections:
            sections[canonical] += "\n" + body
        else:
            sections[canonical] = body

    return sections


def _match_canonical_key(heading: str) -> str | None:
    lowered = heading.lower()
    for canonical, keywords in _SECTION_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return canonical
    return None
