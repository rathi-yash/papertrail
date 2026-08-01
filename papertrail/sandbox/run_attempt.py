"""F7 (Stage 2 stretch goal — DO NOT implement until Stage 1 is solid and validated).

Per PRD Section 6 / Day 6 of the build plan: only attempt this once
F1-F6 are working end-to-end against 3-5 real paper+repo pairs.

Intended scope:
    - Spin up the target repo in an isolated Docker container
    - Attempt install + a minimal run using the config extracted in Stage 1
    - On error, feed the error back into an LLM-driven loop that checks
      it against paper/README context and retries, bounded at ~3 attempts
    - Real security surface: this executes arbitrary repo code. Sandbox
      boundaries need to be taken seriously, not just "runs in a
      container" — no mounted secrets, no network access beyond what's
      needed for pip install, resource/time limits on the container.

TODO (do not start until Stage 1 sign-off):
    - def attempt_run(repo_path: Path, config: dict) -> RunResult
    - def build_sandbox_image(repo_path: Path) -> str (image tag)
    - def retry_with_error_feedback(error: str, context: dict, attempt: int) -> dict
      (adjusted config or command to retry with)
"""

raise NotImplementedError(
    "Stage 2 is a stretch goal — implement F1-F6 (Stage 1) first, per PRD.md"
)
