"""
Script 14 - Refresh Static MusicBrainz Reference Tables in PostgreSQL

This script truncates and reloads seven core MusicBrainz `.tsv` source tables:
artist, artist_credit, artist_credit_name, release_group, release_group_secondary_type,
release_group_secondary_type_join, and release.

These tables are used upstream in the soundtrack filtering process and remain static once loaded.

"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from config import (
    PG_HOST,
    PG_PORT,
    PG_DBNAME,
    PG_USER,
    PG_PASSWORD,
    MB_TSV_FILES
)

# --- Build the PostgreSQL connection string ---
DB_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}"
engine = create_engine(DB_URL)

print("🔌 Connecting to PostgreSQL...")

# --- Target tables in preferred recreate/load order ---
static_tables = [
    "artist",
    "artist_credit",
    "artist_credit_name",
    "release_group",
    "release_group_secondary_type",
    "release_group_secondary_type_join",
    "release",
]

with engine.begin() as conn:
    for table in static_tables:
        file_path = MB_TSV_FILES.get(table)
        if not file_path or not os.path.exists(file_path):
            print(f"❌ Missing or invalid file for table '{table}': {file_path}")
            continue

        print(f"\n📅 Processing file for table: {table}")
        print(f"   ➔ {file_path}")

        try:
            df = pd.read_csv(file_path, sep="\t", dtype=str, na_values="\\N", quoting=3, engine="python")
        except Exception as e:
            print(f"❌ Failed to read {file_path}: {e}")
            continue

        print(f"🧹 Dropping and recreating table {table}...")
        conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE;"))

        columns = [f'"{col}" TEXT' for col in df.columns]
        create_stmt = f"""
        CREATE TABLE {table} (
            {', '.join(columns)}
        );
        """
        conn.execute(text(create_stmt))

        print(f"📄 Inserting {len(df):,} rows into {table}...")
        df.to_sql(table, con=conn, if_exists="append", index=False, method="multi")

print("\n✅ Static MusicBrainz tables refreshed.")
