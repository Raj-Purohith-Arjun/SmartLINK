import os
import pandas as pd
import duckdb

def load_profiles(csv_path='ingest/users.csv'):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    print("[INFO] Loading profiles from CSV...")
    profiles = pd.read_csv(csv_path, sep=',')

    print(profiles.head())  # <--- add this to see the data

    con = duckdb.connect("smartlink.duckdb")
    con.execute("DROP TABLE IF EXISTS users;")
    con.execute("CREATE TABLE users AS SELECT * FROM profiles")

    print(f"[SUCCESS] Loaded {len(profiles)} profiles into DuckDB.")
    return con

if __name__ == "__main__":
    load_profiles()



import pandas as pd

df = pd.read_csv('data/users.csv')
print(df.head())
print(df.columns)
