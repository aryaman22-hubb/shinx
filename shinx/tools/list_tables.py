from typing import Any

from shinx.db import DatabaseAdapter
from shinx.tools.base import Tool


def create_list_tables_tool(adapter: DatabaseAdapter) -> Tool:
    def list_tables(schema_name: str = "public") -> dict[str, Any]:
        tables = adapter.list_table_names(schema_name)
        return {"schema": schema_name, "tables": tables}

    return Tool(
        name="list_tables",
        description="Lists all user tables present in the database schema.",
        parameters={
            "type": "object",
            "properties": {
                "schema_name": {
                    "type": "string",
                    "description": "The schema name, defaults to 'public'.",
                    "default": "public",
                }
            },
        },
        func=list_tables,
    )
