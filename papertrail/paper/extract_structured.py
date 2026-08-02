"""F2: LLM-based structured extraction from isolated paper sections.

This is the highest-risk step in the whole pipeline (per PRD Section
7.1 and Section 11 Risks). Takes the section dict from
extract_text.isolate_relevant_sections() and returns structured JSON
via llm.client (BYOK-routed: Claude if key present, else local
fallback).

The model is instructed to only extract values explicitly stated in
the text, not infer/guess ones that aren't present. Papers with
ambiguous/missing sections return a partial result (empty fields,
"partial": True) rather than failing the whole run.
"""

import json
import re

_EMPTY_RESULT = {
    "hyperparameters": [],
    "dataset": None,
    "hardware": None,
    "environment_notes": None,
}

_PROMPT_TEMPLATE = """You are extracting reproduction details from a machine learning \
paper's text. Only extract values that are EXPLICITLY stated in the text below — do \
not infer or guess values that aren't present.

Return ONLY a JSON object with this exact shape, nothing else:
{{
  "hyperparameters": [{{"name": str, "value": str, "source_text": str}}, ...],
  "dataset": {{"name": str, "link": str or null}} or null,
  "hardware": str or null,
  "environment_notes": str or null
}}

Paper sections:
{sections_text}
"""


def extract_structured(sections: dict[str, str], llm_client) -> dict:
    """Extract structured hyperparameter/dataset/environment data via the LLM client."""
    if not sections:
        return {**_EMPTY_RESULT, "partial": True}

    sections_text = "\n\n".join(
        f"## {name}\n{text}" for name, text in sections.items()
    )
    prompt = _PROMPT_TEMPLATE.format(sections_text=sections_text)

    response_text = llm_client.complete(prompt)
    parsed = _parse_json_response(response_text)
    if parsed is None:
        return {**_EMPTY_RESULT, "partial": True}

    return {**_EMPTY_RESULT, **parsed, "partial": False}


def _parse_json_response(response_text: str) -> dict | None:
    stripped = response_text.strip()
    fence_match = re.match(r"^```(?:json)?\s*\n(.*)\n```$", stripped, re.DOTALL)
    if fence_match:
        stripped = fence_match.group(1).strip()

    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return None
