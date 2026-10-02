import json

from shinx.db import DatabaseAdapter
from shinx.shared.models.plan_node import PlanNode
from shinx.shared.models.db_metadata import DBMetadata

class DBService:
    def __init__(self, database_adapter: DatabaseAdapter) -> None:
        self._database_adapter = database_adapter

    def explain(self, query: str) -> PlanNode | None :
        try: 
            return self._database_adapter.explain(query)
        except Exception as e:
            error = f"Error running explain query: {e}"
            print(error)
            return None

        # Uncomment incase you need to print it
        # with open("explain.json", "w", encoding="utf-8") as f:
        #     json.dump(
        #         explain_output.model_dump(),
        #         f, 
        #         indent= 2
        #     )


    def crawl(self) -> DBMetadata | None:
        try:
            return self._database_adapter.get_database_structure()
        except Exception as e:
            error = f"Error crawling the database: {e}"
            print(error)
            return None

        # Uncomment incase you need to print it
        # with open("database_structure.json", "w", encoding="utf-8") as f:
        #     json.dump(
        #         db_info.model_dump(),
        #         f,
        #         indent=2,
        #     )

    