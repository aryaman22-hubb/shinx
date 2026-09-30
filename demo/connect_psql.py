# We need from the database:
# 
# 1. Database and server info
# PostgreSQL version
# database name
# current schema/search_path
# available extensionsc
# 
# 2. Logical structure
# Tables, Schemas
# Columns, Data types
# Nullability
# Constraints
# Defaults
# 
# 3. Indexes
# Index name
# table, columns, column order, unqiue, primary, partial, expression, index method, predicate, included columns
# 
# 4. Views
#
# these are deferred for now
# 5. stats
# number of distinct values
# null fraction
# most common value


# relevant queries

# 1. database and server info
# SELECT version(); 
# PostgreSQL 18.6 (Ubuntu 18.6-0ubuntu0.26.04.1) on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 15.2.0-16ubuntu1) 15.2.0, 64-bit

# 2. current schema/search_path
# SHOW search_path()

# 3. extensions
# SELECT * FROM pg_available_extensions;
#         name        | default_version | installed_version |                                comment                                 
# --------------------+-----------------+-------------------+------------------------------------------------------------------------
#  pg_prewarm         | 1.2             |                   | prewarm relation data
#  pgstattuple        | 1.5             |                   | show tuple-level statistics
#  sslinfo            | 1.2             |                   | information about SSL certificates
#  autoinc            | 1.0             |                   | functions for autoincrementing fields
 
# 4. tables, schemas
# SELECT
#             table_schema,
#             table_name
#         FROM information_schema.tables
#         WHERE table_type = 'BASE TABLE'
#           AND table_schema NOT IN ('pg_catalog', 'information_schema', 'msar')
#         ORDER BY table_schema, table_name;
# 
# 5. Columns, Data types
# SELECT
#     column_name,
#     data_type,
#     is_nullable,
#     column_default
# FROM information_schema.columns
# WHERE table_schema = 'public'
#   AND table_name = 'users'
# ORDER BY ordinal_position;
# 
# 6. Constraints
# SELECT
#     constraint_name,
#     constraint_type
# FROM information_schema.table_constraints
# WHERE table_schema = 'public'
#   AND table_name = 'users';
# 
# 7. Indexes
# SELECT
#     indexname,
#     indexdef
# FROM pg_indexes
# WHERE schemaname = 'public'
#   AND tablename = 'users';
# 
# 8. Views
# SELECT
#     table_schema,
#     table_name
# FROM information_schema.views
# WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
# ORDER BY table_schema, table_name;

import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="postgres"
)

with conn.cursor() as cur:
    # get versions
    print("Versions:")
    cur.execute("""
        SELECT version(); 
    """)

    print(cur.fetchall())
    print("="*30)
    print("Search Path:")
    
    cur.execute("""
        SHOW search_path;
    """)
    print(cur.fetchall())

    cur.execute("""
        SELECT * FROM pg_available_extensions;
    """)
    print("="*30)
    print("Available extensions: ")
    print("name,default_version,installed,version,comment")

    for name, default_version, installed_version, comment in cur.fetchall():
        print(name, default_version, installed_version, comment)

    cur.execute("""
        SELECT
            table_schema,
            table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
          AND table_schema NOT IN ('pg_catalog', 'information_schema', 'msar')
        ORDER BY table_schema, table_name;
    """)
    print("="*30)
    print("Schemas and tables: ")
    print("schema,table")
    tables_and_schemas = cur.fetchall()
    for schema, table in tables_and_schemas:
        print(schema, table)

    print("="*30)
    print("Table Info: ")    
    for schema, table in tables_and_schemas:
        cur.execute(f"""
                SELECT
                    column_name,
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = '{schema}'
                AND table_name = '{table}'
                ORDER BY ordinal_position;
            """)
        print(f"Table {table}: ")    
        print("-"*30)
        print(f"Columns: ")    
        print('column_name', 'data_type', 'is_nullable', 'column_default')

        for column_name, data_type, is_nullable, column_default in cur.fetchall():
            print(column_name, data_type, is_nullable, column_default)
        print("-"*30)
        print(f"Constraints: ")   
        cur.execute(f"""
                SELECT
                    constraint_name,
                    constraint_type
                FROM information_schema.table_constraints
                WHERE table_schema = '{schema}'
                AND table_name = '{table}';
            """)     
        for constraint_name, constraint_type in cur.fetchall():
            print(constraint_name, constraint_type)
        print("-"*30)
        print(f"Indexes: ")   
        cur.execute(f"""
                SELECT
                    indexname,
                    indexdef
                FROM pg_indexes
                WHERE schemaname = '{schema}'
                AND tablename = '{table}';
            """)     
        for indexname, indexdef in cur.fetchall():
            print(indexname, indexdef)        
        print("\n\n")
            
        
    cur.execute("""
        SELECT
            table_schema,
            table_name
        FROM information_schema.views
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name;
    """)
    print("="*30)
    print("Views: ")
    print("table_schema,table_name")
    for table_schema,table_name in cur.fetchall():
        print(table_schema, table_name)

conn.close()