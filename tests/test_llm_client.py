"""Tests for papertrail.llm.client BYOK routing."""

from papertrail.llm.client import ClaudeClient, get_client
from papertrail.llm.local_model import LocalModel


def test_get_client_returns_claude_client_when_api_key_passed():
    client = get_client(api_key="fake-key")

    assert isinstance(client, ClaudeClient)
    assert client.backend_name == "claude"


def test_get_client_reads_api_key_from_env(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-key-from-env")

    client = get_client()

    assert isinstance(client, ClaudeClient)


def test_get_client_falls_back_to_local_model_when_no_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    client = get_client()

    assert isinstance(client, LocalModel)
    assert client.backend_name == "local"


class _FakeContentBlock:
    def __init__(self, text):
        self.text = text


class _FakeMessage:
    def __init__(self, text):
        self.content = [_FakeContentBlock(text)]


class _FakeMessages:
    def __init__(self, response_text):
        self._response_text = response_text
        self.last_call_kwargs = None

    def create(self, **kwargs):
        self.last_call_kwargs = kwargs
        return _FakeMessage(self._response_text)


class _FakeAnthropicClient:
    def __init__(self, response_text):
        self.messages = _FakeMessages(response_text)


def test_claude_client_complete_returns_response_text():
    fake_sdk_client = _FakeAnthropicClient(response_text="hello from claude")
    client = ClaudeClient(api_key="fake-key", sdk_client=fake_sdk_client)

    result = client.complete("say hello")

    assert result == "hello from claude"
    assert fake_sdk_client.messages.last_call_kwargs["messages"] == [
        {"role": "user", "content": "say hello"}
    ]
