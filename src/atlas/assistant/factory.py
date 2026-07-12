"""Composition root for language-model providers."""

from atlas.assistant.types import LanguageModel
from atlas.config.models import LLMSettings


def create_language_model(settings: LLMSettings) -> LanguageModel:
    """Create the configured model without leaking provider details to callers."""
    if settings.provider == "openai":
        from atlas.assistant.providers.openai import OpenAILanguageModel

        return OpenAILanguageModel(settings)
    raise ValueError(f"Unsupported LLM provider: {settings.provider}")
