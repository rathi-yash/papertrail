"""Tests for papertrail.cli.

Uses click's CliRunner and monkeypatches the pipeline functions the
CLI wires together (each of those functions is unit-tested on its own
elsewhere) so this test verifies wiring/output, not extraction logic.
"""

import json

from click.testing import CliRunner

import papertrail.cli as cli_module
from papertrail.cli import main


class _FakeClient:
    def complete(self, prompt: str) -> str:
        return json.dumps(
            {
                "hyperparameters": [{"name": "lr", "value": "0.0002", "source_text": "lr 2e-4"}],
                "dataset": None,
                "hardware": None,
                "environment_notes": None,
            }
        )


def test_extract_command_prints_structured_json(monkeypatch):
    monkeypatch.setattr(cli_module, "fetch_paper", lambda source: b"%PDF fake content")
    monkeypatch.setattr(cli_module, "extract_full_text", lambda path: "full text")
    monkeypatch.setattr(
        cli_module, "isolate_relevant_sections", lambda text: {"hyperparameters": "lr 2e-4"}
    )
    monkeypatch.setattr(
        cli_module, "get_client", lambda api_key=None, google_api_key=None: _FakeClient()
    )

    runner = CliRunner()
    result = runner.invoke(main, ["extract", "https://arxiv.org/abs/2106.09685"])

    assert result.exit_code == 0
    output = json.loads(result.output)
    assert output["partial"] is False
    assert output["hyperparameters"][0]["name"] == "lr"


def test_extract_command_passes_api_key_override(monkeypatch):
    monkeypatch.setattr(cli_module, "fetch_paper", lambda source: b"%PDF fake content")
    monkeypatch.setattr(cli_module, "extract_full_text", lambda path: "full text")
    monkeypatch.setattr(cli_module, "isolate_relevant_sections", lambda text: {})

    captured = {}

    def fake_get_client(api_key=None, google_api_key=None):
        captured["api_key"] = api_key
        captured["google_api_key"] = google_api_key
        return _FakeClient()

    monkeypatch.setattr(cli_module, "get_client", fake_get_client)

    runner = CliRunner()
    runner.invoke(main, ["extract", "somepaper.pdf", "--api-key", "override-key"])

    assert captured["api_key"] == "override-key"


def test_extract_command_passes_google_api_key_override(monkeypatch):
    monkeypatch.setattr(cli_module, "fetch_paper", lambda source: b"%PDF fake content")
    monkeypatch.setattr(cli_module, "extract_full_text", lambda path: "full text")
    monkeypatch.setattr(cli_module, "isolate_relevant_sections", lambda text: {})

    captured = {}

    def fake_get_client(api_key=None, google_api_key=None):
        captured["google_api_key"] = google_api_key
        return _FakeClient()

    monkeypatch.setattr(cli_module, "get_client", fake_get_client)

    runner = CliRunner()
    runner.invoke(main, ["extract", "somepaper.pdf", "--google-api-key", "override-google-key"])

    assert captured["google_api_key"] == "override-google-key"
