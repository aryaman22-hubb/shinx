from abc import ABC, abstractmethod
from typing import Any

from shinx.shared.models.llm import LLMMessage, LLMResponse


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(
        self,
        messages: list[LLMMessage],
        tools: list[dict[str, Any]] | None = None,
    ) -> LLMResponse:
        """Generates a response from the LLM, either containing tool calls or final content."""
        ...
