"""OpenAI Responses API adapter."""

from typing import Any, Protocol, cast

from openai import APIConnectionError, APIStatusError, APITimeoutError, AuthenticationError, OpenAI

from atlas.assistant.errors import ModelProviderError
from atlas.assistant.types import ModelResponse, ModelUsage
from atlas.config.models import LLMSettings


class OpenAIResponse(Protocol):
    id: str
    output_text: str
    usage: Any


class ResponsesResource(Protocol):
    def create(self, **kwargs: Any) -> OpenAIResponse: ...


class OpenAIClient(Protocol):
    responses: ResponsesResource


class OpenAILanguageModel:
    """Generate provider-neutral text using OpenAI's Responses API."""

    def __init__(self, settings: LLMSettings, *, client: OpenAIClient | None = None) -> None:
        self._settings = settings
        self._client = client or cast(
            OpenAIClient,
            OpenAI(timeout=settings.timeout_seconds, max_retries=settings.max_retries),
        )

    def generate(
        self,
        prompt: str,
        *,
        instructions: str,
        previous_response_id: str | None = None,
    ) -> ModelResponse:
        request: dict[str, Any] = {
            "model": self._settings.model,
            "instructions": instructions,
            "input": prompt,
            "reasoning": {"effort": self._settings.reasoning_effort},
            "text": {"verbosity": self._settings.verbosity},
            "max_output_tokens": self._settings.max_output_tokens,
        }
        if previous_response_id is not None:
            request["previous_response_id"] = previous_response_id
        try:
            response = self._client.responses.create(**request)
        except AuthenticationError as error:
            raise ModelProviderError(
                "authentication", "OpenAI API key is missing or invalid."
            ) from error
        except APITimeoutError as error:
            raise ModelProviderError("timeout", "OpenAI request timed out. Try again.") from error
        except APIConnectionError as error:
            raise ModelProviderError("connection", "Could not connect to OpenAI.") from error
        except APIStatusError as error:
            error_code = getattr(error, "code", None)
            if error.status_code == 429 and error_code == "insufficient_quota":
                raise ModelProviderError(
                    "quota", "OpenAI quota exhausted. Check API billing and limits."
                ) from error
            if error.status_code == 429:
                raise ModelProviderError(
                    "rate_limit", "OpenAI rate limit reached. Try again shortly."
                ) from error
            raise ModelProviderError(
                "provider", f"OpenAI request failed ({error.status_code})."
            ) from error

        usage = None
        if response.usage is not None:
            usage = ModelUsage(
                response.usage.input_tokens,
                response.usage.output_tokens,
                response.usage.total_tokens,
            )
        return ModelResponse(response.output_text, response.id, usage)
