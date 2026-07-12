from pathlib import Path

import pytest
from pydantic import ValidationError

from atlas.config import load_settings


def test_loads_yaml_and_environment_override(tmp_path: Path) -> None:
    config = tmp_path / "atlas.yaml"
    config.write_text("llm:\n  provider: openai\nlogging:\n  level: INFO\n", encoding="utf-8")

    settings = load_settings(config, environment={"ATLAS_LLM__MODEL": "test-model"})

    assert settings.llm.model == "test-model"
    assert settings.logging.level == "INFO"


def test_rejects_unknown_configuration(tmp_path: Path) -> None:
    config = tmp_path / "atlas.yaml"
    config.write_text("voice:\n  typo: value\n", encoding="utf-8")

    with pytest.raises(ValidationError):
        load_settings(config, environment={})


def test_missing_file_uses_defaults(tmp_path: Path) -> None:
    settings = load_settings(tmp_path / "missing.yaml", environment={})

    assert settings.voice.wake_word == "atlas"
    assert settings.llm.provider == "openai"


@pytest.mark.parametrize(
    "llm_yaml",
    [
        "provider: unsupported",
        'model: ""',
        'model: "   "',
        "max_output_tokens: 0",
        "timeout_seconds: 0",
        "max_retries: 6",
        "reasoning_effort: extreme",
    ],
)
def test_rejects_invalid_llm_configuration(tmp_path: Path, llm_yaml: str) -> None:
    config = tmp_path / "atlas.yaml"
    config.write_text(f"llm:\n  {llm_yaml}\n", encoding="utf-8")

    with pytest.raises(ValidationError):
        load_settings(config, environment={})
