from typing import Any

from shinx.services.providers.base import BaseLLMProvider
from shinx.shared.models.llm import LLMMessage, LLMResponse


class LLMService:
    def __init__(self, provider: BaseLLMProvider) -> None:
        self._provider = provider

    def generate(
        self,
        messages: list[LLMMessage],
        tools: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        return self._provider.generate(messages, tools)
