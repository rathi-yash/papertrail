"""CLI entry point.

Currently implemented:
    papertrail extract <arxiv-url-or-pdf-path>   (F1, F2)

Target (once F3-F5 land):
    papertrail check <arxiv-url> <repo-url>

TODO:
    - Add `check` subcommand once repo.* / crossref.* / report.* exist
    - Add --output-dir flag (default: ./reports) for `check`
"""

import json
import tempfile
from pathlib import Path

import click

from papertrail.llm.client import get_client
from papertrail.paper.extract_structured import extract_structured
from papertrail.paper.extract_text import extract_full_text, isolate_relevant_sections
from papertrail.paper.fetch import fetch_paper


@click.group()
def main() -> None:
    """PaperTrail: reproducibility gap-finder for ML papers + repos."""


@main.command()
@click.argument("source")
@click.option(
    "--api-key",
    default=None,
    help="Anthropic API key (overrides ANTHROPIC_API_KEY env var).",
)
@click.option(
    "--google-api-key",
    default=None,
    help="Google (Gemini) API key (overrides GOOGLE_API_KEY env var). "
    "Used if no Anthropic key is available.",
)
def extract(source: str, api_key: str | None, google_api_key: str | None) -> None:
    """Extract structured hyperparameter/dataset/environment data from SOURCE.

    SOURCE is an arXiv URL (e.g. https://arxiv.org/abs/2106.09685) or a
    local PDF path.
    """
    pdf_bytes = fetch_paper(source)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name
    try:
        text = extract_full_text(tmp_path)
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    sections = isolate_relevant_sections(text)
    client = get_client(api_key=api_key, google_api_key=google_api_key)
    result = extract_structured(sections, client)

    click.echo(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
