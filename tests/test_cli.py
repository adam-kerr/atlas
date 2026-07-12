from pathlib import Path

import pytest
from typer.testing import CliRunner

from atlas.assistant import LanguageModel
from atlas.assistant.errors import ModelProviderError
from atlas.assistant.types import ModelResponse
from atlas.cli import app


class FakeLanguageModel:
    def generate(
        self, prompt: str, *, instructions: str, previous_response_id: str | None = None
    ) -> ModelResponse:
        return ModelResponse(f"Atlas heard: {prompt}", "response-1")


def test_ask_prints_model_response(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config = tmp_path / "atlas.yaml"
    config.write_text("logging:\n  format: text\n", encoding="utf-8")

    def fake_create_language_model(settings: object) -> LanguageModel:
        return FakeLanguageModel()

    monkeypatch.setattr("atlas.cli.create_language_model", fake_create_language_model)

    result = CliRunner().invoke(app, ["ask", "hello", "--config", str(config)])

    assert result.exit_code == 0
    assert result.stdout == "Atlas heard: hello\n"


def test_chat_handles_commands(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config = tmp_path / "atlas.yaml"
    config.write_text("logging:\n  format: text\n", encoding="utf-8")
    monkeypatch.setattr("atlas.cli.create_language_model", lambda settings: FakeLanguageModel())

    result = CliRunner().invoke(
        app, ["chat", "--config", str(config)], input="hello\n/status\n/new\n/exit\n"
    )

    assert result.exit_code == 0
    assert "Atlas: Atlas heard: hello" in result.stdout
    assert "Conversation: active" in result.stdout
    assert "Started a new conversation." in result.stdout


def test_ask_prints_concise_provider_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    class FailingLanguageModel(FakeLanguageModel):
        def generate(
            self, prompt: str, *, instructions: str, previous_response_id: str | None = None
        ) -> ModelResponse:
            raise ModelProviderError("quota", "OpenAI quota exhausted.")

    config = tmp_path / "atlas.yaml"
    config.write_text("logging:\n  format: text\n", encoding="utf-8")
    monkeypatch.setattr("atlas.cli.create_language_model", lambda settings: FailingLanguageModel())

    result = CliRunner().invoke(app, ["ask", "hello", "--config", str(config)])

    assert result.exit_code == 1
    assert "Error: OpenAI quota exhausted." in result.stderr
    assert "Traceback" not in result.output
