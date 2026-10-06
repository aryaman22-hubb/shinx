from shinx.db import DatabaseAdapter
from shinx.shared.models.plan_node import PlanNode
from shinx.shared.models.db_metadata import DBMetadata


class DBService:
    def __init__(self, database_adapter: DatabaseAdapter) -> None:
        self._database_adapter = database_adapter

    def explain(self, query: str) -> PlanNode | None:
        try:
            return self._database_adapter.explain(query)
        except Exception as e:
            print(f"Error running explain query: {e}")
            return None

    def crawl(self) -> DBMetadata | None:
        try:
            return self._database_adapter.get_database_structure()
        except Exception as e:
            print(f"Error crawling the database: {e}")
            return None