from pathlib import Path

import pytest
from typer.testing import CliRunner

from atlas.assistant import LanguageModel
from atlas.cli import app


class FakeLanguageModel:
    def generate(self, prompt: str, *, instructions: str) -> str:
        return f"Atlas heard: {prompt}"


def test_ask_prints_model_response(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    config = tmp_path / "atlas.yaml"
    config.write_text("logging:\n  format: text\n", encoding="utf-8")

    def fake_create_language_model(settings: object) -> LanguageModel:
        return FakeLanguageModel()

    monkeypatch.setattr("atlas.cli.create_language_model", fake_create_language_model)

    result = CliRunner().invoke(app, ["ask", "hello", "--config", str(config)])

    assert result.exit_code == 0
    assert result.stdout == "Atlas heard: hello\n"
