from shinx.db import DatabaseAdapter

class CrawlingService:
    def __init__(self, database_adapter: DatabaseAdapter) -> None:
        self._database_adapter = database_adapter

    def crawl(self) -> None:
        try:
            db_info = self._database_adapter.get_database_info()
        except Exception as e:
            print("Error fetching database info:", e)
            return

        print("Database Info:")
        print("  Version:", db_info.get("version"))
        print("  Search Path:", db_info.get("search_path"))
        print("  Extensions:")
        for ext in db_info.get("extensions", []):
            name = ext.get("name")
            inst = ext.get("installed_version")
            default = ext.get("default_version")
            comment = ext.get("comment")
            print(f"    - {name} (installed: {inst}, default: {default}) - {comment}")

        try:
            tables = self._database_adapter.get_tables()
        except Exception as e:
            print("Error fetching tables:", e)
            tables = []

        print(f"\nTables ({len(tables)}):")
        for t in tables:
            schema = t.get("schema")
            table = t.get("table")
            print(f"\nTable: {schema}.{table}")

            try:
                columns = self._database_adapter.get_columns(schema, table)
            except Exception as e:
                print("  Error fetching columns:", e)
                columns = []

            print("  Columns:")
            for c in columns:
                print(
                    "   -",
                    f"{c.get('column_name')}:{c.get('data_type')}",
                    f"nullable={c.get('is_nullable')}",
                    f"default={c.get('column_default')}",
                )

            try:
                constraints = self._database_adapter.get_constraints(schema, table)
            except Exception as e:
                print("  Error fetching constraints:", e)
                constraints = []

            if constraints:
                print("  Constraints:")
                for c in constraints:
                    print(f"   - {c.get('constraint_name')}: {c.get('constraint_type')}")

            try:
                indexes = self._database_adapter.get_indexes(schema, table)
            except Exception as e:
                print("  Error fetching indexes:", e)
                indexes = []

            if indexes:
                print("  Indexes:")
                for i in indexes:
                    print(f"   - {i.get('indexname')}: {i.get('indexdef')}")

        try:
            views = self._database_adapter.get_views()
        except Exception as e:
            print("Error fetching views:", e)
            views = []

        print(f"\nViews ({len(views)}):")
        for v in views:
            print(f"  - {v.get('schema')}.{v.get('view')}")

    