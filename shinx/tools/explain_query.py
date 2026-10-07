import re
from typing import Any

from shinx.db import DatabaseAdapter
from shinx.tools.base import Tool

FORBIDDEN_SQL_PATTERN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|GRANT|REVOKE|CREATE)\b",
    re.IGNORECASE,
)


def create_explain_query_tool(adapter: DatabaseAdapter) -> Tool:
    def explain_query(query: str) -> dict[str, Any]:
        cleaned = query.strip()
        if FORBIDDEN_SQL_PATTERN.search(cleaned):
            return {"error": "Only read-only SELECT queries can be explained for security reasons."}

        plan = adapter.explain(cleaned)
        if plan is None:
            return {"error": "Failed to generate query execution plan."}
        return plan.model_dump()

    return Tool(
        name="explain_query",
        description="Explains a SQL query to retrieve its execution plan (costs, scan types, rows, filters, join conditions).",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The exact SQL SELECT query to explain.",
                }
            },
            "required": ["query"],
        },
        func=explain_query,
    )
