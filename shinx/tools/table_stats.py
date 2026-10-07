from typing import Any

from shinx.db import DatabaseAdapter
from shinx.tools.base import Tool


def create_table_stats_tool(adapter: DatabaseAdapter) -> Tool:
    def get_table_stats(table_name: str, schema_name: str = "public") -> dict[str, Any]:
        return adapter.get_table_stats(table_name, schema_name)

    return Tool(
        name="get_table_stats",
        description="Fetches table-specific statistics including current row count and disk size. Crucial for assessing whether optimization/indexing is warranted based on table volume.",
        parameters={
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "The name of the table to check row count and stats for.",
                },
                "schema_name": {
                    "type": "string",
                    "description": "The schema name, defaults to 'public'.",
                    "default": "public",
                },
            },
            "required": ["table_name"],
        },
        func=get_table_stats,
    )
