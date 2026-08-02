"""Tests for papertrail.paper.extract_text.

Uses the real LoRA paper PDF fixture (examples/lora_paper/2106.09685.pdf)
per PRD.md Section 8 / test_paper_extraction.py TODOs.
"""

from pathlib import Path

from papertrail.paper.extract_text import extract_full_text, isolate_relevant_sections

LORA_PDF = Path(__file__).parent.parent / "examples" / "lora_paper" / "2106.09685.pdf"


def test_extract_full_text_returns_nonempty_string():
    text = extract_full_text(str(LORA_PDF))

    assert isinstance(text, str)
    assert "LoRA" in text


def test_isolate_relevant_sections_finds_hyperparameters_section():
    text = extract_full_text(str(LORA_PDF))

    sections = isolate_relevant_sections(text)

    assert "hyperparameters" in sections
    assert "warmup" in sections["hyperparameters"].lower()
