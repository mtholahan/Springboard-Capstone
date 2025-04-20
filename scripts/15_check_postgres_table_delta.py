"""
Script 15 - Compare Expected vs. Existing PostgreSQL Tables

This utility script compares the tables loaded by your Capstone pipeline (defined in config.py)
against the full list of user-owned tables in the 'public' schema of your PostgreSQL database.

It outputs:
- All tables found in the database
- Tables refreshed via scripts 13/14
- Tables present in the DB but not refreshed (possibly stale)
- Tables expected by config.py but missing from the DB

Helpful for ensuring your environment is complete and self-rebuildable.

"""

from sqlalchemy import create_engine, text
import pandas as pd
from config import (
    PG_USER,
    PG_PASSWORD,
    PG_PORT,
    PG_DB,
    PG_HOST,
    REFRESH_INPUTS,
)

# Connect to Postgres
DB_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
engine = create_engine(DB_URL)

# Step 1: Get all user tables in 'public' schema
query = text("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
ORDER BY table_name;
""")

with engine.connect() as conn:
    result = conn.execute(query)
    user_tables = sorted([row[0] for row in result.fetchall()])

refreshed_tables = sorted(REFRESH_INPUTS.keys())
only_in_db = sorted(set(user_tables) - set(refreshed_tables))
only_in_config = sorted(set(refreshed_tables) - set(user_tables))

print("\n🧾 All user tables in 'public':")
print(user_tables)

print("\n✅ Tables refreshed via script 13:")
print(refreshed_tables)

print("\n❗ Tables in Postgres but NOT refreshed in script 13:")
print(only_in_db)

print("\n⚠️ Tables defined in config.py but NOT present in Postgres:")
print(only_in_config)
