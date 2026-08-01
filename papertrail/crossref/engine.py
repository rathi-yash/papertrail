"""F4: diff paper-extracted hyperparameters against repo-extracted config.

Produces matched / missing / mismatched findings, each confidence-tagged:
    - high confidence: direct structural match/mismatch (e.g. paper says
      lr=2e-4, repo default is --lr 0.0002 -> matched, deterministic)
    - low confidence: required fuzzy name-normalization or LLM judgment
      to link paper prose to a repo field (e.g. paper's "Dropout Prob"
      vs. repo's `lora_dropout` flag)

Also checks:
    - dataset link liveness + whether repo references/handles it
    - environment/dependency completeness

TODO:
    - def cross_reference(paper_data: dict, repo_data: dict) -> list[Finding]
    - Finding should carry: field name, paper value, repo value, status
      (matched/missing/mismatched), confidence (high/low), and a short
      human-readable note
    - Fuzzy name matching: start with a simple normalization (lowercase,
      strip underscores/prefixes) before reaching for LLM-assisted matching
    - Reference case: PRD.md Section 8 (LoRA prototype) — the paper's
      "Warmup Steps: 500" vs. repo's "--warmup_step 500" should match at
      high confidence; the repo's "--random_seed 110" with no paper
      counterpart should surface as a "repo has undocumented pin" finding
"""
