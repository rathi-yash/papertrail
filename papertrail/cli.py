"""CLI entry point.

Usage (target):
    papertrail check <arxiv-url> <repo-url>

Wires together F1-F5 from the PRD:
    paper.fetch + paper.extract_text + paper.extract_structured  (F1, F2)
    repo.clone + repo.parse_readme + repo.parse_config           (F3)
    crossref.engine                                              (F4)
    report.generate                                              (F5)

TODO:
    - Add `check` subcommand (click) accepting arxiv_url, repo_url
    - Add --api-key flag as an override for ANTHROPIC_API_KEY env var
    - Add --output-dir flag (default: ./reports)
    - Wire the pipeline end to end, print report to stdout, save to reports/
"""


def main() -> None:
    raise NotImplementedError("CLI not yet implemented — see TODOs in this file and PRD.md")


if __name__ == "__main__":
    main()
