import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
    repo_root = Path(__file__).resolve().parent.parent
    load_dotenv(repo_root / ".env")
    load_dotenv(repo_root / "shinx" / ".env")
except ImportError:
    pass

from shinx.agents.optimizer_agent import OptimizerAgent
from shinx.db import DatabaseAdapter
from shinx.services.llm import get_llm_provider
from shinx.shared.models.db_metadata import Column, Constraint, DBMetadata, Index, TableMetaData
from shinx.shared.models.plan_node import PlanNode
from shinx.tools import create_db_tool_registry


class SampleMockDatabaseAdapter(DatabaseAdapter):
    def close(self) -> None:
        pass

    def get_database_structure(self) -> DBMetadata:
        return DBMetadata(version="16.2", extensions=[], tables=[], views=[])

    def explain(self, query: str) -> PlanNode:
        return PlanNode(
            node_type="Seq Scan",
            startup_cost=0.0,
            total_cost=8420.5,
            estimated_rows=125000,
            relation_name="orders",
            alias="orders",
            filter="(customer_id = 42 AND created_at >= '2026-01-01'::date)",
            extra={"Filter": "(customer_id = 42 AND created_at >= '2026-01-01'::date)"},
        )

    def _get_database_info(self) -> dict:
        return {"version": "PostgreSQL 16.2", "extensions": [{"name": "btree_gist", "installed_version": "1.8"}]}

    def _get_tables(self) -> list[TableMetaData]:
        return []

    def _get_columns(self, schema, table) -> list[Column]:
        if table == "orders":
            return [
                Column(name="id", data_type="bigint", is_nullable="NO", column_default="nextval('orders_id_seq')"),
                Column(name="customer_id", data_type="integer", is_nullable="NO", column_default=""),
                Column(name="total_amount", data_type="numeric(10,2)", is_nullable="NO", column_default="0.00"),
                Column(name="status", data_type="character varying(32)", is_nullable="NO", column_default="'PENDING'"),
                Column(name="created_at", data_type="timestamp without time zone", is_nullable="NO", column_default="now()"),
            ]
        return []

    def _get_constraints(self, schema, table) -> list[Constraint]:
        return [Constraint(name="orders_pkey", type="PRIMARY KEY")]

    def _get_indexes(self, schema, table) -> list[Index]:
        return [
            Index(name="orders_pkey", indexdef="CREATE UNIQUE INDEX orders_pkey ON public.orders USING btree (id)")
        ]

    def _get_views(self) -> list:
        return []

    def get_database_info(self) -> dict:
        return self._get_database_info()

    def list_table_names(self, schema_name: str = "public") -> list[str]:
        return ["orders", "customers", "order_items"]

    def get_table_metadata(self, table_name: str, schema_name: str = "public") -> TableMetaData | None:
        if table_name == "orders":
            return TableMetaData(
                name="orders",
                schema_name="public",
                columns=self._get_columns(schema_name, table_name),
                constraints=self._get_constraints(schema_name, table_name),
                indexes=self._get_indexes(schema_name, table_name),
            )
        return None

    def get_table_stats(self, table_name: str, schema_name: str = "public") -> dict:
        if table_name == "orders":
            return {
                "table_name": "orders",
                "schema_name": "public",
                "row_count": 125000,
                "disk_size": "45 MB",
                "dead_tuples": 350,
            }
        return {"error": f"Table '{table_name}' not found"}


def print_report(report):
    print("\n" + "=" * 60)
    print(" SHINX OPTIMIZATION REPORT (Agent 1 Output)")
    print("=" * 60)
    print(f"Target Query:\n  {report.query.strip()}\n")
    print(f"Bottleneck Identified:\n  {report.bottleneck_identified}\n")
    print(f"Database Engine:\n  {report.database_engine or 'N/A'}\n")
    print("-" * 60)
    print("Suggestions:")
    for idx, s in enumerate(report.suggestions, 1):
        print(f"\n[{idx}] {s.title} ({s.type})")
        print(f"    Impact: {s.impact} | Confidence: {s.confidence * 100:.0f}%")
        print(f"    Explanation: {s.explanation}")
        if s.suggested_sql:
            print(f"    Suggested SQL:\n      {s.suggested_sql}")
        if s.trade_offs:
            print(f"    Trade-offs: {s.trade_offs}")
    print("=" * 60 + "\n")


def main():
    query = """
    SELECT *
    FROM orders
    WHERE customer_id = 42
      AND created_at >= '2026-01-01'
    ORDER BY created_at DESC;
    """

    adapter = SampleMockDatabaseAdapter()
    tools = create_db_tool_registry(adapter)

    has_api_key = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    if not has_api_key:
        print("[!] Note: GEMINI_API_KEY is not detected in environment.")
        print("    Running offline simulated verification...\n")
        from tests.test_optimizer_agent import ScriptedMockLLMProvider
        llm = ScriptedMockLLMProvider()
    else:
        llm = get_llm_provider()

    agent = OptimizerAgent(llm=llm, tools=tools, verbose=True)
    report = agent.optimize(query)
    print_report(report)


if __name__ == "__main__":
    main()
