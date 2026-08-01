"""F3 (part 2): parse README(s) for stated setup/usage details.

Looks for reproduction commands (e.g. shell blocks showing how to run
training/eval), which is often where the real hyperparameter defaults
live — see the LoRA prototype in PRD.md Section 8, where
examples/NLG/README.md's command block was the ground truth we
cross-referenced against.

TODO:
    - def parse_readme(repo_path: Path) -> dict
      (find README.md at root and in subdirectories like examples/;
      extract code blocks, especially ones that look like CLI
      invocations with flags)
    - def extract_cli_args_from_command(command_text: str) -> dict[str, str]
      (parse "--flag value" pairs out of a shell command block)
"""
