from shinx.db import DatabaseAdapter

import psycopg

class PostgresAdapter(DatabaseAdapter):
    def __init__(self, host, port, dbname, user, password):
        super().__init__()
        conn = psycopg.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
        )
        self._connection = conn        

    def close(self) -> None:
        if self._connection:
            try:
                self._connection.close()
            finally:
                self._connection = None

    def _ensure_connected(self):
        if not self._connection:
            raise RuntimeError("Not connected to a PostgreSQL database")

    def get_database_info(self):
        self._ensure_connected()
        with self._connection.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]

            cur.execute("SHOW search_path;")
            search_path = cur.fetchone()[0]

            cur.execute("SELECT name, default_version, installed_version, comment FROM pg_available_extensions;")
            extensions = [
                {
                    "name": row[0],
                    "default_version": row[1],
                    "installed_version": row[2],
                    "comment": row[3],
                }
                for row in cur.fetchall()
            ]

        return {"version": version, "search_path": search_path, "extensions": extensions}

    def get_tables(self):
        self._ensure_connected()
        query = """
        SELECT
            table_schema,
            table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
          AND table_schema NOT IN ('pg_catalog', 'information_schema', 'msar')
        ORDER BY table_schema, table_name;
        """
        with self._connection.cursor() as cur:
            cur.execute(query)
            return [ {"schema": s, "table": t} for s, t in cur.fetchall() ]

    def get_columns(self, schema, table):
        self._ensure_connected()
        query = f"""
            SELECT
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = %s
            AND table_name = %s
            ORDER BY ordinal_position;
        """
        with self._connection.cursor() as cur:
            cur.execute(query, (schema, table))
            return [
                {
                    "column_name": row[0],
                    "data_type": row[1],
                    "is_nullable": row[2],
                    "column_default": row[3],
                }
                for row in cur.fetchall()
            ]

    def get_constraints(self, schema, table):
        self._ensure_connected()
        query = f"""
            SELECT
                constraint_name,
                constraint_type
            FROM information_schema.table_constraints
            WHERE table_schema = %s
            AND table_name = %s;
        """
        with self._connection.cursor() as cur:
            cur.execute(query, (schema, table))
            return [ {"constraint_name": r[0], "constraint_type": r[1]} for r in cur.fetchall() ]

    def get_indexes(self, schema, table):
        self._ensure_connected()
        query = f"""
            SELECT
                indexname,
                indexdef
            FROM pg_indexes
            WHERE schemaname = %s
            AND tablename = %s;
        """
        with self._connection.cursor() as cur:
            cur.execute(query, (schema, table))
            return [ {"indexname": r[0], "indexdef": r[1]} for r in cur.fetchall() ]

    def get_views(self):
        self._ensure_connected()
        query = """
        SELECT
            table_schema,
            table_name
        FROM information_schema.views
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name;
        """
        with self._connection.cursor() as cur:
            cur.execute(query)
            return [ {"schema": s, "view": v} for s, v in cur.fetchall() ]

        