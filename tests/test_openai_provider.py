from dataclasses import dataclass

import pytest

from atlas.assistant.providers.openai import OpenAILanguageModel


@dataclass
class FakeResponse:
    output_text: str


class FakeResponsesResource:
    def __init__(self, output_text: str = "Hello from OpenAI") -> None:
        self.output_text = output_text
        self.request: dict[str, str] | None = None

    def create(self, *, model: str, instructions: str, input: str) -> FakeResponse:
        self.request = {"model": model, "instructions": instructions, "input": input}
        return FakeResponse(self.output_text)


class FakeOpenAIClient:
    def __init__(self, responses: FakeResponsesResource) -> None:
        self.responses = responses


def test_generates_text_through_responses_api() -> None:
    responses = FakeResponsesResource()
    model = OpenAILanguageModel("test-model", client=FakeOpenAIClient(responses))

    result = model.generate("hello", instructions="Be concise.")

    assert result == "Hello from OpenAI"
    assert responses.request == {
        "model": "test-model",
        "instructions": "Be concise.",
        "input": "hello",
    }


def test_surfaces_provider_failure() -> None:
    class FailingResponsesResource(FakeResponsesResource):
        def create(self, *, model: str, instructions: str, input: str) -> FakeResponse:
            raise RuntimeError("provider unavailable")

    client = FakeOpenAIClient(FailingResponsesResource())
    model = OpenAILanguageModel("test-model", client=client)

    with pytest.raises(RuntimeError, match="provider unavailable"):
        model.generate("hello", instructions="Be concise.")
