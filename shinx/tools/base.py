from typing import Any, Sequence
from langchain_core.tools import BaseTool

# Alias for backward compatibility without creating custom dataclasses
Tool = BaseTool


class ToolRegistry:
    """Registry managing LangChain BaseTool instances."""

    def __init__(self, tools: Sequence[BaseTool] | None = None):
        self._tools: dict[str, BaseTool] = {}
        if tools:
            for tool in tools:
                self.register(tool)

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def execute(self, name: str, arguments: dict[str, Any]) -> Any:
        tool = self.get(name)
        if not tool:
            return {"error": f"Tool '{name}' not found in registry"}
        try:
            return tool.invoke(arguments)
        except Exception as e:
            return {"error": f"Tool execution error in '{name}': {str(e)}"}

    def get_all_tools(self) -> list[BaseTool]:
        return list(self._tools.values())

    def to_langchain_tools(self) -> list[BaseTool]:
        """Returns all registered tools directly as native LangChain BaseTool instances."""
        return list(self._tools.values())

    def to_schemas(self) -> list[dict[str, Any]]:
        """Returns standard function JSON schemas for the registered tools."""
        schemas = []
        for tool in self._tools.values():
            schemas.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.args_schema.schema() if tool.args_schema else {},
                },
            })
        return schemas

    def __iter__(self):
        return iter(self._tools.values())

    def __len__(self) -> int:
        return len(self._tools)
