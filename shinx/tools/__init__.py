from shinx.db import DatabaseAdapter
from shinx.tools.base import Tool, ToolRegistry
from shinx.tools.explain_query import create_explain_query_tool
from shinx.tools.inspect_table import create_inspect_table_tool
from shinx.tools.table_stats import create_table_stats_tool
from shinx.tools.list_tables import create_list_tables_tool
from shinx.tools.database_info import create_database_info_tool


def create_db_tool_registry(adapter: DatabaseAdapter) -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(create_explain_query_tool(adapter))
    registry.register(create_inspect_table_tool(adapter))
    registry.register(create_table_stats_tool(adapter))
    registry.register(create_list_tables_tool(adapter))
    registry.register(create_database_info_tool(adapter))
    return registry


__all__ = [
    "Tool",
    "ToolRegistry",
    "create_db_tool_registry",
    "create_explain_query_tool",
    "create_inspect_table_tool",
    "create_table_stats_tool",
    "create_list_tables_tool",
    "create_database_info_tool",
]
