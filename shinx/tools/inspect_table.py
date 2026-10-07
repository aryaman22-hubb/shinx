from typing import Any

from shinx.db import DatabaseAdapter
from shinx.tools.base import Tool


def create_inspect_table_tool(adapter: DatabaseAdapter) -> Tool:
    def inspect_table(table_name: str, schema_name: str = "public") -> dict[str, Any]:
        table_meta = adapter.get_table_metadata(table_name, schema_name)
        if table_meta is None:
            return {"error": f"Table '{table_name}' in schema '{schema_name}' was not found."}

        data = table_meta.model_dump()
        try:
            stats = adapter.get_table_stats(table_name, schema_name)
            data["stats"] = stats
        except Exception:
            pass

        return data

    return Tool(
        name="inspect_table",
        description="Inspects complete context for a specific table: row count, columns, data types, nullability, constraints, and existing indexes.",
        parameters={
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "The name of the table to inspect.",
                },
                "schema_name": {
                    "type": "string",
                    "description": "The schema name, defaults to 'public'.",
                    "default": "public",
                },
            },
            "required": ["table_name"],
        },
        func=inspect_table,
    )
