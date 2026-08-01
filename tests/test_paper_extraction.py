"""Tests for papertrail.paper.

Primary fixture: examples/lora_paper/ — the manually-validated LoRA
paper (arXiv:2106.09685) prototype from PRD.md Section 8. Structured
extraction on this paper should reliably recover at minimum: batch
size, learning rate, weight decay, epochs, warmup steps, LoRA rank,
LoRA alpha, and label smoothing, matching examples/lora_paper/expected_output.json.

TODO:
    - test_extract_text_finds_hyperparameter_section (LoRA Section D)
    - test_extract_structured_matches_expected_output (against fixture)
    - test_handles_paper_with_no_clear_hyperparameter_section
      (graceful partial-result behavior, not a crash)
"""
