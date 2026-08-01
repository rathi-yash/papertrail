"""Local open-weight model fallback (free tier), used when no API key is set.

Per PRD: something in the Qwen3 or Llama 3.x instruct 7-8B class,
run locally via transformers. Expect meaningfully weaker performance
than Claude on ambiguous/messy paper prose — this should be reflected
as lower confidence in report output, not hidden.

TODO:
    - class LocalModel implementing the same .complete() interface as
      the Claude-backed client in client.py
    - Model choice + loading (consider quantization for reasonable
      local inference speed/memory)
    - Clear one-time warning/log when this fallback is active, so the
      user knows they're on the free/lower-quality path
"""
