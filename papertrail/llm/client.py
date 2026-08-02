"""BYOK routing: Claude, then free-tier Gemini, then local HF fallback.

Precedence (per PRD Section 7.3, extended with a free-tier middle option):
    1. ANTHROPIC_API_KEY env var (or --api-key CLI flag override) set
       -> use Claude API, best extraction quality
    2. GOOGLE_API_KEY env var (or --google-api-key CLI flag override) set
       -> use Gemini's free tier, no local compute required
    3. Otherwise -> fall back to local_model.py (free, weaker on messy
       prose)

All extraction call sites (paper/extract_structured.py, and any future
crossref LLM-assisted matching) should go through get_client() rather
than calling Claude, Gemini, or the local model directly, so the
fallback logic lives in exactly one place.
"""

import os

import anthropic
from google import genai

from papertrail.llm.local_model import LocalModel

_DEFAULT_CLAUDE_MODEL = "claude-sonnet-4-5"
_DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"


class ClaudeClient:
    backend_name = "claude"

    def __init__(self, api_key: str, sdk_client=None, model: str = _DEFAULT_CLAUDE_MODEL):
        self._sdk_client = sdk_client or anthropic.Anthropic(api_key=api_key)
        self._model = model

    def complete(self, prompt: str, max_tokens: int = 4096) -> str:
        message = self._sdk_client.messages.create(
            model=self._model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text


class GeminiClient:
    backend_name = "gemini"

    def __init__(self, api_key: str, sdk_client=None, model: str = _DEFAULT_GEMINI_MODEL):
        self._sdk_client = sdk_client or genai.Client(api_key=api_key)
        self._model = model

    def complete(self, prompt: str) -> str:
        response = self._sdk_client.models.generate_content(
            model=self._model,
            contents=prompt,
        )
        return response.text


def get_client(api_key: str | None = None, google_api_key: str | None = None):
    """Return the best available client: Claude, then Gemini, then local fallback."""
    resolved_anthropic_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if resolved_anthropic_key:
        return ClaudeClient(api_key=resolved_anthropic_key)

    resolved_google_key = google_api_key or os.environ.get("GOOGLE_API_KEY")
    if resolved_google_key:
        return GeminiClient(api_key=resolved_google_key)

    return LocalModel()
