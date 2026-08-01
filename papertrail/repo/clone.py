"""F3 (part 1): clone the target GitHub repo to a temp working directory.

TODO:
    - def clone_repo(repo_url: str) -> Path (temp dir containing the clone)
    - Shallow clone (--depth 1) since we don't need full history for v1
    - Clean up temp dir after the pipeline run completes (context manager
      or explicit cleanup call from cli.py)
"""
