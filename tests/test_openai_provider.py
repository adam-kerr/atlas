from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

import pytest

from atlas.assistant.providers.openai import OpenAILanguageModel
from atlas.config.models import LLMSettings


@dataclass
class FakeResponse:
    id: str
    output_text: str
    usage: Any


class FakeResponsesResource:
    def __init__(self, output_text: str = "Hello from OpenAI") -> None:
        self.output_text = output_text
        self.request: dict[str, Any] | None = None

    def create(self, **kwargs: Any) -> FakeResponse:
        self.request = kwargs
        usage = SimpleNamespace(input_tokens=10, output_tokens=5, total_tokens=15)
        return FakeResponse("response-1", self.output_text, usage)


class FakeOpenAIClient:
    def __init__(self, responses: FakeResponsesResource) -> None:
        self.responses = responses


def test_generates_text_through_responses_api() -> None:
    responses = FakeResponsesResource()
    settings = LLMSettings(model="test-model")
    model = OpenAILanguageModel(settings, client=FakeOpenAIClient(responses))

    result = model.generate("hello", instructions="Be concise.", previous_response_id="previous-1")

    assert result.text == "Hello from OpenAI"
    assert result.response_id == "response-1"
    assert result.usage is not None
    assert result.usage.total_tokens == 15
    assert responses.request == {
        "model": "test-model",
        "instructions": "Be concise.",
        "input": "hello",
        "reasoning": {"effort": "none"},
        "text": {"verbosity": "low"},
        "max_output_tokens": 300,
        "previous_response_id": "previous-1",
    }


def test_surfaces_provider_failure() -> None:
    class FailingResponsesResource(FakeResponsesResource):
        def create(self, **kwargs: Any) -> FakeResponse:
            raise RuntimeError("provider unavailable")

    client = FakeOpenAIClient(FailingResponsesResource())
    model = OpenAILanguageModel(LLMSettings(model="test-model"), client=client)

    with pytest.raises(RuntimeError, match="provider unavailable"):
        model.generate("hello", instructions="Be concise.")
