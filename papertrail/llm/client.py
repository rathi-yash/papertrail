"""BYOK routing: Claude if the user supplies a key, else local HF fallback.

Precedence (per PRD Section 7.3):
    1. ANTHROPIC_API_KEY env var (or --api-key CLI flag override) set
       -> use Claude API, best extraction quality
    2. Otherwise -> fall back to local_model.py (free, weaker on messy
       prose)

All extraction call sites (paper/extract_structured.py, and any future
crossref LLM-assisted matching) should go through get_client() rather
than calling Claude or the local model directly, so the fallback logic
lives in exactly one place.
"""

import os

import anthropic

from papertrail.llm.local_model import LocalModel

_DEFAULT_MODEL = "claude-sonnet-4-5"


class ClaudeClient:
    backend_name = "claude"

    def __init__(self, api_key: str, sdk_client=None, model: str = _DEFAULT_MODEL):
        self._sdk_client = sdk_client or anthropic.Anthropic(api_key=api_key)
        self._model = model

    def complete(self, prompt: str, max_tokens: int = 4096) -> str:
        message = self._sdk_client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text


def get_client(api_key: str | None = None):
    """Return a Claude-backed client if a key is available, else the local fallback."""
    resolved_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if resolved_key:
        return ClaudeClient(api_key=resolved_key)
    return LocalModel()
