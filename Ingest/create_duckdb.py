# ingest/create_duckdb.py

import duckdb
import pandas as pd
import os

# Path setup
csv_path = os.path.join("ingest", "users.csv")
duckdb_path = os.path.join("ingest", "duckdb_file.duckdb")

# Load CSV
df = pd.read_csv(csv_path)

# Write to DuckDB
conn = duckdb.connect(database=duckdb_path, read_only=False)
conn.execute("DROP TABLE IF EXISTS users;")
conn.execute("""
CREATE TABLE users AS SELECT * FROM df
""")
print("DuckDB database created at:", duckdb_path)
