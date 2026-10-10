import inspect
import json
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    func: Callable[..., Any]

    def to_schema(self) -> dict[str, Any]:
        """Returns standard JSON Schema representation of the tool."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def execute(self, **kwargs) -> Any:
        try:
            result = self.func(**kwargs)
            if hasattr(result, "model_dump"):
                return result.model_dump()
            return result
        except Exception as e:
            return {"error": f"Tool execution error in '{self.name}': {str(e)}"}


    def to_langchain_tool(self):
        """Converts this Tool into a native LangChain StructuredTool."""
        from langchain_core.tools import StructuredTool

        return StructuredTool.from_function(
            func=self.func,
            name=self.name,
            description=self.description,
        )


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def execute(self, name: str, arguments: dict[str, Any]) -> Any:
        tool = self.get(name)
        if not tool:
            return {"error": f"Tool '{name}' not found in registry"}
        return tool.execute(**arguments)

    def get_all_tools(self) -> list[Tool]:
        return list(self._tools.values())

    def to_schemas(self) -> list[dict[str, Any]]:
        return [tool.to_schema() for tool in self._tools.values()]

    def to_langchain_tools(self) -> list[Any]:
        """Returns all registered tools converted to LangChain StructuredTool format."""
        return [tool.to_langchain_tool() for tool in self._tools.values()]

