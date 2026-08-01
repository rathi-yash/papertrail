"""BYOK routing: Claude if the user supplies a key, else local HF fallback.

Precedence (per PRD Section 7.3):
    1. ANTHROPIC_API_KEY env var (or --api-key CLI flag override) set
       -> use Claude API, best extraction quality
    2. Otherwise -> fall back to local_model.py (free, weaker on messy
       prose)

All extraction call sites (paper/extract_structured.py, and any future
crossref LLM-assisted matching) should go through this module rather
than calling Claude or the local model directly, so the fallback logic
lives in exactly one place.

TODO:
    - class LLMClient with a single method: .complete(prompt: str, ...) -> str
      (or structured output variant returning parsed JSON)
    - def get_client(api_key: str | None = None) -> LLMClient
      (checks env var, then falls back to local_model.LocalModel)
    - Tag responses with which backend served them, so report.generate
      can reflect backend in the confidence tagging (Claude-served
      extractions can lean higher confidence than local-model ones)
"""
