"""Provider-neutral configuration models."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class StrictModel(BaseModel):
    """Base model that rejects misspelled and unsupported settings."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class VoiceSettings(StrictModel):
    wake_word: str = "atlas"
    stt_provider: str = "whisper"
    tts_provider: str = "piper"


class LLMSettings(StrictModel):
    provider: Literal["openai"] = "openai"
    model: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] = "gpt-5.6-luna"
    reasoning_effort: Literal["none", "low", "medium", "high"] = "none"
    verbosity: Literal["low", "medium", "high"] = "low"
    max_output_tokens: int = Field(default=300, ge=1, le=16_384)
    timeout_seconds: float = Field(default=30, gt=0, le=300)
    max_retries: int = Field(default=1, ge=0, le=5)


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
