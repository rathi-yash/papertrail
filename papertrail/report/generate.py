"""F5: turn crossref findings into a human-readable report.

Two outputs:
    - CLI-printed summary (concise, colored status icons if feasible)
    - Saved Markdown/JSON report in ./reports/

TODO:
    - def generate_report(findings: list[Finding], paper_meta: dict, repo_meta: dict) -> Report
    - def print_cli_summary(report: Report) -> None
    - def save_report(report: Report, output_dir: Path) -> Path
    - Format: checklist style, e.g.
        ✅ learning_rate: matches (0.0002)
        ⚠️  warmup_steps: paper doesn't state a value paper-side match unclear
        ❌ dataset_link: dead link, no repo-side fallback mentioned
      grouped by confidence, with a one-line summary at the top
      ("7 matched, 1 missing, 1 mismatched, 1 undocumented repo pin")
"""
