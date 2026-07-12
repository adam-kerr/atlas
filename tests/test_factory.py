import pytest

from atlas.assistant.factory import create_language_model
from atlas.config.models import LLMSettings


def test_rejects_unsupported_provider_defensively() -> None:
    settings = LLMSettings.model_construct(provider="unsupported", model="test-model")

    with pytest.raises(ValueError, match="Unsupported LLM provider: unsupported"):
        create_language_model(settings)
