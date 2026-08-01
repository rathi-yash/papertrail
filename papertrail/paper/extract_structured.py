"""F2: LLM-based structured extraction from isolated paper sections.

This is the highest-risk step in the whole pipeline (per PRD Section 7.1
and Section 11 Risks). Prototype this against several real papers,
including at least one messy/poorly-documented one, before building
the rest of the pipeline on top of it.

Takes the section dict from extract_text.isolate_relevant_sections()
and returns structured JSON:
    {
        "hyperparameters": [{"name": str, "value": str, "source_text": str}, ...],
        "dataset": {"name": str, "link": str | None},
        "hardware": str | None,
        "environment_notes": str | None
    }

Uses llm.client (BYOK-routed: Claude if key present, else local fallback).

TODO:
    - def extract_structured(sections: dict[str, str], llm_client) -> dict
    - Design the extraction prompt: instruct the model to only extract
      values explicitly stated in the text, not infer/guess ones that
      aren't there (avoid hallucinated hyperparameters)
    - Validate output against examples/lora_paper/expected_output.json
    - Handle papers where sections are ambiguous/missing gracefully —
      return partial results with a flag, don't fail the whole run
"""
