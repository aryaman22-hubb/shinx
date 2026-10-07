from typing import Any

from shinx.db import DatabaseAdapter
from shinx.tools.base import Tool


def create_database_info_tool(adapter: DatabaseAdapter) -> Tool:
    def get_database_info() -> dict[str, Any]:
        return adapter.get_database_info()

    return Tool(
        name="get_database_info",
        description="Fetches database version and installed extensions.",
        parameters={"type": "object", "properties": {}},
        func=get_database_info,
    )
