import re

import psycopg

from shinx.db import DatabaseAdapter
from shinx.shared.models.db_metadata import (
    Column,
    Constraint,
    DBMetadata,
    Extension,
    Index,
    TableMetaData,
    View,
    ViewColumn,
)


class PostgresAdapter(DatabaseAdapter):
    def __init__(self, host, port, dbname, user, password):
        super().__init__()
        self._connection = psycopg.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
        )

    def close(self) -> None:
        if self._connection:
            try:
                self._connection.close()
            finally:
                self._connection = None

    def _ensure_connected(self):
        if not self._connection:
            raise RuntimeError("Not connected to a PostgreSQL database")

    @staticmethod
    def _extract_version(version_output: str) -> str:
        match = re.search(r"PostgreSQL\s+(\d+(?:\.\d+)?)", version_output)
        if match:
            return match.group(1)
        return version_output.strip()

    def _get_search_path(self) -> str:
        self._ensure_connected()
        conn = self._connection
        if conn is None:
            raise RuntimeError("Not connected to a PostgreSQL database")
        with conn.cursor() as cur:
            cur.execute("SHOW search_path;")
            row = cur.fetchone()
            if row is None:
                return ""
            return row[0]

    def _get_database_info(self) -> dict:
        self._ensure_connected()
        conn = self._connection
        if conn is None:
            raise RuntimeError("Not connected to a PostgreSQL database")
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version_row = cur.fetchone()
            if version_row is None:
                raise RuntimeError("Could not fetch PostgreSQL version")
            version = self._extract_version(version_row[0])

            cur.execute(
                "SELECT name, default_version, installed_version, comment FROM pg_available_extensions;"
            )
            extensions = [
                {
                    "name": row[0],
                    "default_version": row[1],
                    "installed_version": row[2],
                    "comment": row[3],
                }
                for row in cur.fetchall()
            ]

        return {"version": version, "extensions": extensions}

    def get_database_structure(self) -> DBMetadata:
        self._ensure_connected()
        database_info = self._get_database_info()
        tables = self._get_tables()
        views = self._get_views()

        return DBMetadata(
            version=database_info["version"],
            extensions=[Extension(**item) for item in database_info["extensions"]],
            tables=tables,
            views=views,
        )

    def _get_tables(self) -> list[TableMetaData]:
        self._ensure_connected()
        conn = self._connection
        if conn is None:
            raise RuntimeError("Not connected to a PostgreSQL database")
        query = """
        SELECT
            table_schema,
            table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
          AND table_schema NOT IN ('pg_catalog', 'information_schema', 'msar')
        ORDER BY table_schema, table_name;
        """
        with conn.cursor() as cur:
            cur.execute(query)
            return [
                TableMetaData(
                    name=t,
                    schema_name=s,
                    columns=self._get_columns(s, t),
                    constraints=self._get_constraints(s, t),
                    indexes=self._get_indexes(s, t),
                )
                for s, t in cur.fetchall()
            ]

    def get_tables(self) -> list[TableMetaData]:
        return self._get_tables()

    def _get_columns(self, schema, table) -> list[Column]:
        self._ensure_connected()
        conn = self._connection
        if conn is None:
            raise RuntimeError("Not connected to a PostgreSQL database")
        query = """
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
        with conn.cursor() as cur:
            cur.execute(query, (schema, table))
            return [
                Column(
                    name=row[0],
                    data_type=row[1],
                    is_nullable=row[2],
                    column_default=row[3] or "",
                )
                for row in cur.fetchall()
            ]

    def _get_constraints(self, schema, table) -> list[Constraint]:
        self._ensure_connected()
        conn = self._connection
        if conn is None:
            raise RuntimeError("Not connected to a PostgreSQL database")
        query = """
            SELECT
                constraint_name,
                constraint_type
            FROM information_schema.table_constraints
            WHERE table_schema = %s
            AND table_name = %s;
        """
        with conn.cursor() as cur:
            cur.execute(query, (schema, table))
            return [
                Constraint(name=row[0], type=row[1])
                for row in cur.fetchall()
            ]

    def get_constraints(self, schema, table):
        return self._get_constraints(schema, table)

    def _get_indexes(self, schema, table) -> list[Index]:
        self._ensure_connected()
        conn = self._connection
        if conn is None:
            raise RuntimeError("Not connected to a PostgreSQL database")
        query = """
            SELECT
                indexname,
                indexdef
            FROM pg_indexes
            WHERE schemaname = %s
            AND tablename = %s;
        """
        with conn.cursor() as cur:
            cur.execute(query, (schema, table))
            return [
                Index(name=row[0], indexdef=row[1])
                for row in cur.fetchall()
            ]

    def get_indexes(self, schema, table):
        return self._get_indexes(schema, table)

    def _get_views(self) -> list[View]:
        self._ensure_connected()
        conn = self._connection
        if conn is None:
            raise RuntimeError("Not connected to a PostgreSQL database")

        view_query = """
        SELECT
            schemaname,
            viewname,
            viewowner,
            definition
        FROM pg_catalog.pg_views
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
        ORDER BY schemaname, viewname;
        """

        with conn.cursor() as cur:
            cur.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'information_schema'
                  AND table_name = 'views';
            """)
            available_view_columns = {row[0] for row in cur.fetchall()}

            view_info_fields = [
                "table_schema",
                "table_name",
                "is_updatable",
                "is_insertable_into",
                "is_trigger_updatable",
                "is_trigger_deletable",
                "is_trigger_insertable",
            ]
            selected_view_info_fields = [
                field for field in view_info_fields if field in available_view_columns
            ]

            view_info_query = f"""
            SELECT
                {', '.join(selected_view_info_fields)}
            FROM information_schema.views
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema');
            """

            view_columns_query = """
            SELECT
                table_schema,
                table_name,
                column_name,
                ordinal_position,
                data_type,
                is_nullable
            FROM information_schema.columns
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY table_schema, table_name, ordinal_position;
            """

            matview_query = """
            SELECT
                schemaname,
                matviewname,
                matviewowner,
                definition,
                tablespace
            FROM pg_catalog.pg_matviews
            WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
            ORDER BY schemaname, matviewname;
            """

            description_query = """
            SELECT
                n.nspname AS schema_name,
                c.relname AS view_name,
                obj_description(c.oid, 'pg_class') AS description
            FROM pg_catalog.pg_class c
            JOIN pg_catalog.pg_namespace n
                ON n.oid = c.relnamespace
            WHERE c.relkind = 'v'
              AND n.nspname NOT IN ('pg_catalog', 'information_schema');
            """

            cur.execute(view_query)
            pg_views = {
                (schema_name, view_name): {
                    "owner": owner,
                    "definition": definition,
                }
                for schema_name, view_name, owner, definition in cur.fetchall()
            }

            if selected_view_info_fields:
                cur.execute(view_info_query)
                info_map = {}
                for row in cur.fetchall():
                    row_data = dict(zip(selected_view_info_fields, row))
                    key = (row_data["table_schema"], row_data["table_name"])
                    info_map[key] = {
                        "is_updatable": row_data.get("is_updatable"),
                        "is_insertable_into": row_data.get("is_insertable_into"),
                        "is_trigger_updatable": row_data.get("is_trigger_updatable"),
                        "is_trigger_deletable": row_data.get("is_trigger_deletable"),
                        "is_trigger_insertable": row_data.get("is_trigger_insertable"),
                    }
            else:
                info_map = {}

            cur.execute(view_columns_query)
            columns_map: dict[tuple[str, str], list[ViewColumn]] = {}
            for schema_name, view_name, column_name, ordinal_position, data_type, is_nullable in cur.fetchall():
                key = (schema_name, view_name)
                columns_map.setdefault(key, []).append(
                    ViewColumn(
                        column_name=column_name,
                        ordinal_position=ordinal_position,
                        data_type=data_type,
                        is_nullable=is_nullable,
                    )
                )

            cur.execute(matview_query)
            matviews = {
                (schema_name, matview_name): {
                    "owner": owner,
                    "definition": definition,
                    "tablespace": tablespace,
                }
                for schema_name, matview_name, owner, definition, tablespace in cur.fetchall()
            }

            cur.execute(description_query)
            descriptions = {
                (schema_name, view_name): description
                for schema_name, view_name, description in cur.fetchall()
            }

        view_names = set(pg_views) | set(info_map) | set(columns_map) | set(descriptions) | set(matviews)
        views: list[View] = []
        for schema_name, view_name in sorted(view_names):
            key = (schema_name, view_name)
            pg_view = pg_views.get(key, {})
            info = info_map.get(key, {})
            desc = descriptions.get(key)
            view_columns = columns_map.get(key, [])
            matview = matviews.get(key)

            owner = pg_view.get("owner")
            definition = pg_view.get("definition")
            if not owner and matview:
                owner = matview.get("owner")
            if not definition and matview:
                definition = matview.get("definition")

            view = View(
                name=view_name,
                schema_name=schema_name,
                owner=owner,
                definition=definition,
                is_updatable=info.get("is_updatable"),
                is_insertable_into=info.get("is_insertable_into"),
                is_trigger_updatable=info.get("is_trigger_updatable"),
                is_trigger_deletable=info.get("is_trigger_deletable"),
                is_trigger_insertable=info.get("is_trigger_insertable"),
                is_materialized=matview is not None,
                description=desc,
                columns=view_columns,
            )
            views.append(view)

        return views

    def get_views(self):
        return self._get_views()
