"""Local open-weight model fallback (free tier), used when no API key is set.

Per PRD: something in the Qwen3 or Llama 3.x instruct 7-8B class, run
locally via transformers. Expect meaningfully weaker performance than
Claude on ambiguous/messy paper prose — this should be reflected as
lower confidence in report output, not hidden.

Not yet implemented: model choice/loading is a separate piece of work
(see PRD Section 7.3). Construction succeeds so BYOK routing can be
tested end-to-end; .complete() raises until a backing model is wired up.
"""


class LocalModel:
    backend_name = "local"

    def complete(self, prompt: str) -> str:
        raise NotImplementedError(
            "Local model fallback is not yet implemented — set ANTHROPIC_API_KEY "
            "to use the Claude-backed client instead."
        )
