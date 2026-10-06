import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="postgres",
)

with conn.cursor() as cur:
    print("Versions:")
    cur.execute("SELECT version();")
    print(cur.fetchall())
    print("=" * 30)

    print("Search Path:")
    cur.execute("SHOW search_path;")
    print(cur.fetchall())
    print("=" * 30)

    cur.execute("SELECT * FROM pg_available_extensions;")
    print("Available extensions:")
    print("name,default_version,installed,version,comment")
    for name, default_version, installed_version, comment in cur.fetchall():
        print(name, default_version, installed_version, comment)
    print("=" * 30)

    cur.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
          AND table_schema NOT IN ('pg_catalog', 'information_schema', 'msar')
        ORDER BY table_schema, table_name;
    """)
    print("Schemas and tables:")
    tables_and_schemas = cur.fetchall()
    for schema, table in tables_and_schemas:
        print(schema, table)
    print("=" * 30)

    print("Table Info:")
    for schema, table in tables_and_schemas:
        cur.execute(f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = '{schema}'
              AND table_name = '{table}'
            ORDER BY ordinal_position;
        """)
        print(f"Table {table}:")
        print("-" * 30)
        print("Columns:")
        for column_name, data_type, is_nullable, column_default in cur.fetchall():
            print(column_name, data_type, is_nullable, column_default)
        print("-" * 30)

        print("Constraints:")
        cur.execute(f"""
            SELECT constraint_name, constraint_type
            FROM information_schema.table_constraints
            WHERE table_schema = '{schema}'
              AND table_name = '{table}';
        """)
        for constraint_name, constraint_type in cur.fetchall():
            print(constraint_name, constraint_type)
        print("-" * 30)

        print("Indexes:")
        cur.execute(f"""
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE schemaname = '{schema}'
              AND tablename = '{table}';
        """)
        for indexname, indexdef in cur.fetchall():
            print(indexname, indexdef)
        print("\n\n")

    cur.execute("""
        SELECT table_schema, table_name
        FROM information_schema.views
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name;
    """)
    print("=" * 30)
    print("Views:")
    for table_schema, table_name in cur.fetchall():
        print(table_schema, table_name)

conn.close()