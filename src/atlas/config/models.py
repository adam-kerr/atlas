"""Provider-neutral configuration models."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    """Base model that rejects misspelled and unsupported settings."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class VoiceSettings(StrictModel):
    wake_word: str = "atlas"
    stt_provider: str = "whisper"
    tts_provider: str = "piper"


class LLMSettings(StrictModel):
    provider: str = "openai"
    model: str | None = None


class AssistantSettings(StrictModel):
    personality: str = "concise"


class IntegrationSettings(StrictModel):
    weather: bool = False
    calendar: bool = False
    home_assistant: bool = False


class LoggingSettings(StrictModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    format: Literal["json", "text"] = "json"


class AtlasSettings(StrictModel):
    voice: VoiceSettings = Field(default_factory=VoiceSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    assistant: AssistantSettings = Field(default_factory=AssistantSettings)
    integrations: IntegrationSettings = Field(default_factory=IntegrationSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
