from shinx.db import DatabaseAdapter
import json
class CrawlingService:
    def __init__(self, database_adapter: DatabaseAdapter) -> None:
        self._database_adapter = database_adapter

    def crawl(self) -> None:
        try:
            db_info = self._database_adapter.get_database_structure()
        except Exception as e:
            print("Error fetching database info:", e)
            return

        with open("database_structure.json", "w", encoding="utf-8") as f:
            json.dump(
                db_info.model_dump(),
                f,
                indent=2,
            )

    