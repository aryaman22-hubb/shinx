import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
    repo_root = Path(__file__).resolve().parent.parent.parent
    load_dotenv(repo_root / ".env")
    load_dotenv(repo_root / "shinx" / ".env")
except ImportError:
    pass

from shinx.services.llm.base import BaseLLMProvider, LLMMessage, LLMResponse, ToolCall
from shinx.services.llm.gemini_provider import GeminiProvider


def get_llm_provider(
    api_key: str | None = None,
    model: str | None = None,
) -> BaseLLMProvider:
    """Instantiate the Gemini LLM provider using configuration or environment variables."""
    return GeminiProvider(api_key=api_key, model=model)


__all__ = [
    "BaseLLMProvider",
    "LLMMessage",
    "LLMResponse",
    "ToolCall",
    "GeminiProvider",
    "get_llm_provider",
]
