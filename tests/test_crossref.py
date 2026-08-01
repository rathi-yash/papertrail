"""Tests for papertrail.crossref.

TODO:
    - test_exact_match_high_confidence
      (e.g. paper lr=0.0002, repo --lr 0.0002 -> matched, high confidence)
    - test_fuzzy_name_match
      (paper "Dropout Prob" vs repo `lora_dropout` -> matched, lower
      confidence than an exact key match, per PRD.md Section 8 finding)
    - test_repo_only_field_flagged
      (repo --random_seed 110 with no paper-side counterpart -> flagged
      as "undocumented repo pin", not silently ignored — this was the
      standout finding from the LoRA prototype)
    - test_missing_from_repo_flagged
      (paper states a hyperparameter, repo has no corresponding config
      or default -> flagged as missing)
"""
