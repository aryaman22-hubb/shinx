from langchain_core.tools import BaseTool

from shinx.db import DatabaseAdapter
from shinx.tools.base import Tool, ToolRegistry
from shinx.tools.database_info import create_database_info_tool
from shinx.tools.explain_query import create_explain_query_tool
from shinx.tools.inspect_table import create_inspect_table_tool
from shinx.tools.list_tables import create_list_tables_tool
from shinx.tools.table_stats import create_table_stats_tool


def create_db_tools(adapter: DatabaseAdapter) -> list[BaseTool]:
    """Creates a list of native LangChain tools for database optimization."""
    return [
        create_explain_query_tool(adapter),
        create_inspect_table_tool(adapter),
        create_table_stats_tool(adapter),
        create_list_tables_tool(adapter),
        create_database_info_tool(adapter),
    ]


def create_db_tool_registry(adapter: DatabaseAdapter) -> ToolRegistry:
    """Creates a ToolRegistry containing all native LangChain database optimization tools."""
    return ToolRegistry(create_db_tools(adapter))


__all__ = [
    "BaseTool",
    "Tool",
    "ToolRegistry",
    "create_db_tools",
    "create_db_tool_registry",
    "create_explain_query_tool",
    "create_inspect_table_tool",
    "create_table_stats_tool",
    "create_list_tables_tool",
    "create_database_info_tool",
]
