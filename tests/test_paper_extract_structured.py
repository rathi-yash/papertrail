"""Tests for papertrail.paper.extract_structured (F2).

Uses a fake LLM client (dependency-injected) rather than calling the
real Claude API, so these tests are fast and deterministic. Real
extraction quality against actual papers is validated separately (see
examples/lora_paper/expected_output.json + manual prototyping notes).
"""

import json

from papertrail.paper.extract_structured import extract_structured

_VALID_RESPONSE = json.dumps(
    {
        "hyperparameters": [
            {"name": "batch_size", "value": "8", "source_text": "batch size of 8"},
            {"name": "learning_rate", "value": "0.0002", "source_text": "lr 2e-4"},
        ],
        "dataset": {"name": "E2E NLG", "link": None},
        "hardware": None,
        "environment_notes": None,
    }
)


class _FakeClient:
    def __init__(self, response_text):
        self._response_text = response_text
        self.last_prompt = None

    def complete(self, prompt: str) -> str:
        self.last_prompt = prompt
        return self._response_text


def test_extract_structured_parses_valid_llm_json():
    client = _FakeClient(_VALID_RESPONSE)
    sections = {"hyperparameters": "We use a batch size of 8 and lr 2e-4."}

    result = extract_structured(sections, client)

    assert result["hyperparameters"] == [
        {"name": "batch_size", "value": "8", "source_text": "batch size of 8"},
        {"name": "learning_rate", "value": "0.0002", "source_text": "lr 2e-4"},
    ]
    assert result["dataset"] == {"name": "E2E NLG", "link": None}
    assert result["partial"] is False


def test_extract_structured_includes_section_text_in_prompt():
    client = _FakeClient(_VALID_RESPONSE)
    sections = {"hyperparameters": "We use a batch size of 8 and lr 2e-4."}

    extract_structured(sections, client)

    assert "batch size of 8" in client.last_prompt


def test_extract_structured_strips_markdown_code_fence():
    fenced = "```json\n" + _VALID_RESPONSE + "\n```"
    client = _FakeClient(fenced)
    sections = {"hyperparameters": "some text"}

    result = extract_structured(sections, client)

    assert result["hyperparameters"][0]["name"] == "batch_size"


def test_extract_structured_returns_partial_on_empty_sections():
    client = _FakeClient(_VALID_RESPONSE)

    result = extract_structured({}, client)

    assert result["partial"] is True
    assert result["hyperparameters"] == []
    assert client.last_prompt is None


def test_extract_structured_returns_partial_on_malformed_llm_output():
    client = _FakeClient("not valid json at all")
    sections = {"hyperparameters": "some text"}

    result = extract_structured(sections, client)

    assert result["partial"] is True
    assert result["hyperparameters"] == []
