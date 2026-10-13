import json
from unittest import TestCase, main

from shinx.db import DatabaseAdapter
from shinx.services.llm_service import LLMService
from shinx.services.providers.base import BaseLLMProvider
from shinx.shared.models.db_metadata import Column, Constraint, DBMetadata, Index, TableMetaData
from shinx.shared.models.llm import LLMMessage, LLMResponse, ToolCall
from shinx.shared.models.plan_node import PlanNode
from shinx.shared.models.suggestion import ImpactLevel, OptimizationReport, SuggestionType
from shinx.tools import create_db_tool_registry
from shinx.agents.optimizer_agent import OptimizerAgent


class MockDatabaseAdapter(DatabaseAdapter):
    def close(self) -> None:
        pass

    def get_database_structure(self) -> DBMetadata:
        return DBMetadata(version="16.0", extensions=[], tables=[], views=[])

    def explain(self, query: str) -> PlanNode:
        return PlanNode(
            node_type="Seq Scan",
            startup_cost=0.0,
            total_cost=450.0,
            estimated_rows=50000,
            relation_name="members",
            filter="(email = 'test@example.com')",
        )

    def _get_database_info(self) -> dict:
        return {"version": "PostgreSQL 16.0", "extensions": []}

    def _get_tables(self) -> list[TableMetaData]:
        return []

    def _get_columns(self, schema, table) -> list[Column]:
        return [
            Column(name="id", data_type="integer", is_nullable="NO", column_default=""),
            Column(name="email", data_type="character varying", is_nullable="NO", column_default=""),
            Column(name="created_at", data_type="timestamp", is_nullable="YES", column_default=""),
        ]

    def _get_constraints(self, schema, table) -> list[Constraint]:
        return [Constraint(name="members_pkey", type="PRIMARY KEY")]

    def _get_indexes(self, schema, table) -> list[Index]:
        return [Index(name="members_pkey", indexdef="CREATE UNIQUE INDEX members_pkey ON members(id)")]

    def _get_views(self) -> list:
        return []

    def get_database_info(self) -> dict:
        return self._get_database_info()

    def list_table_names(self, schema_name: str = "public") -> list[str]:
        return ["members", "organizations"]

    def get_table_metadata(self, table_name: str, schema_name: str = "public") -> TableMetaData | None:
        if table_name == "members":
            return TableMetaData(
                name="members",
                schema_name="public",
                columns=self._get_columns(schema_name, table_name),
                constraints=self._get_constraints(schema_name, table_name),
                indexes=self._get_indexes(schema_name, table_name),
            )
        return None

    def get_table_stats(self, table_name: str, schema_name: str = "public") -> dict:
        if table_name == "members":
            return {
                "table_name": "members",
                "schema_name": "public",
                "row_count": 50000,
                "disk_size": "12 MB",
                "dead_tuples": 120,
            }
        return {"error": f"Table '{table_name}' not found."}


class ScriptedMockLLMProvider(BaseLLMProvider):
    def __init__(self):
        self.call_count = 0

    def generate(self, messages: list[LLMMessage], tools=None) -> LLMResponse:
        self.call_count += 1

        if self.call_count == 1:
            return LLMResponse(
                tool_calls=[
                    ToolCall(
                        id="call_1",
                        name="explain_query",
                        arguments={"query": "SELECT * FROM members WHERE email = 'test@example.com';"},
                    )
                ]
            )
        elif self.call_count == 2:
            return LLMResponse(
                tool_calls=[
                    ToolCall(
                        id="call_2",
                        name="inspect_table",
                        arguments={"table_name": "members"},
                    )
                ]
            )
        else:
            final_report = {
                "query": "SELECT * FROM members WHERE email = 'test@example.com';",
                "bottleneck_identified": "Sequential scan on members table due to unindexed email column in WHERE clause.",
                "suggestions": [
                    {
                        "title": "Add index on members(email)",
                        "type": "INDEX_CREATION",
                        "impact": "HIGH",
                        "confidence": 0.95,
                        "explanation": "Creates a B-Tree index on email to convert the full table scan into an Index Scan.",
                        "suggested_sql": "CREATE INDEX idx_members_email ON members(email);",
                        "trade_offs": "Adds slight disk usage and minimal overhead during inserts.",
                    }
                ],
                "database_engine": "PostgreSQL 16.0",
            }
            return LLMResponse(content=json.dumps(final_report))


class TestOptimizerAgent(TestCase):
    def test_agent_investigation_loop(self):
        adapter = MockDatabaseAdapter()
        tools = create_db_tool_registry(adapter)
        mock_provider = ScriptedMockLLMProvider()
        llm_service = LLMService(mock_provider)

        agent = OptimizerAgent(llm=llm_service, tools=tools, verbose=True)
        report = agent.optimize("SELECT * FROM members WHERE email = 'test@example.com';")

        self.assertIsInstance(report, OptimizationReport)
        self.assertEqual(len(report.suggestions), 1)
        suggestion = report.suggestions[0]
        self.assertEqual(suggestion.type, SuggestionType.INDEX_CREATION)
        self.assertEqual(suggestion.impact, ImpactLevel.HIGH)
        self.assertIn("CREATE INDEX idx_members_email", suggestion.suggested_sql)
        self.assertEqual(mock_provider.call_count, 3)

    def test_security_filter_on_mutations(self):
        adapter = MockDatabaseAdapter()
        tools = create_db_tool_registry(adapter)

        result = tools.execute("explain_query", {"query": "DROP TABLE members;"})
        self.assertIn("error", result)
        self.assertIn("Only read-only SELECT queries", result["error"])


if __name__ == "__main__":
    main()
