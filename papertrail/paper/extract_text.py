"""F1 (part 2): extract text and isolate relevant sections from the PDF.

Uses pymupdf (fitz) for raw text extraction, then isolates the sections
that matter for reproduction: experimental setup, hyperparameter tables,
dataset description, hardware/environment notes.

Per PRD: try section-header heuristics first (matching common headers
like "Hyperparameters", "Implementation Details", "Experimental Setup",
"Appendix" subsections), fall back to LLM-assisted isolation only if
heuristics come up empty.

TODO:
    - def extract_full_text(pdf_source: bytes | str) -> str
    - def isolate_relevant_sections(full_text: str) -> dict[str, str]
      (keys like "experimental_setup", "hyperparameters", "dataset",
      "hardware", each mapping to the raw text of that section)
    - Validate against the LoRA paper (arXiv:2106.09685) manual
      prototype from PRD.md Section 8 as a first correctness check —
      Section D ("Hyperparameters Used in Experiments") should be
      reliably found by header heuristics
"""
