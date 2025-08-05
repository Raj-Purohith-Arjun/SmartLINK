# ingest/test_duckdb.py

import duckdb

db_path = 'ingest/duckdb_file.duckdb'
conn = duckdb.connect(database=db_path, read_only=True)

# Show tables
tables = conn.execute("SHOW TABLES").fetchall()
print("Tables in database:", tables)

# Show sample data
try:
    rows = conn.execute("SELECT * FROM users LIMIT 5").fetchall()
    print("\nSample rows from 'users' table:")
    for row in rows:
        print(row)
except Exception as e:
    print("Error querying DuckDB:", e)
