import os
import pprint

from shinx.adapters.postgres_adapter import PostgresAdapter
from shinx.agents.optimizer_agent import OptimizerAgent
from shinx.services.llm_service import LLMService
from shinx.services.providers.gemini_provider import GeminiProvider
from shinx.tools import create_db_tool_registry


def main():
    query = "SELECT * FROM members WHERE status = 'ACTIVE' ORDER BY created_at DESC;"

    print("Connecting to PostgreSQL...")
    try:
        adapter = PostgresAdapter(
            host=os.getenv("PGHOST", "localhost"),
            port=int(os.getenv("PGPORT", "5432")),
            dbname=os.getenv("PGDATABASE", "postgres"),
            user=os.getenv("PGUSER", "postgres"),
            password=os.getenv("PGPASSWORD", "postgres"),
        )
    except Exception as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        print("Tip: Run 'python demo/demo_agent.py' to test the agent with an offline simulated database.")
        return

    tools = create_db_tool_registry(adapter)
    provider = GeminiProvider()
    llm_service = LLMService(provider)
    agent = OptimizerAgent(llm=llm_service, tools=tools, verbose=True)

    print(f"\nRunning Shinx Optimizer Agent for query: {query}\n")
    report = agent.optimize(query)

    print("\n" + "=" * 60)
    print(" SHINX OPTIMIZATION REPORT")
    print("=" * 60)
    pprint.pprint(report.model_dump())


if __name__ == "__main__":
    main()
