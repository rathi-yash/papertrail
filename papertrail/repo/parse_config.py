"""F3 (part 3): parse config files and argparse defaults via Python's ast module.

Covers:
    - YAML/JSON config files anywhere in the repo
    - argparse.add_argument(..., default=...) calls in entry-point scripts
    - requirements.txt / environment.yml for dependency completeness checks

TODO:
    - def parse_yaml_json_configs(repo_path: Path) -> dict
    - def parse_argparse_defaults(repo_path: Path) -> dict
      (walk .py files, use ast to find add_argument calls, extract
      dest/default pairs — this is Python-only per PRD non-goals)
    - def parse_requirements(repo_path: Path) -> dict
      (does requirements.txt/environment.yml exist, are versions pinned)
"""
