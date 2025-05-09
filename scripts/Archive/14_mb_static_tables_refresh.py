"""
14_mb_static_tables_refresh.py

Fast-loads 7 static MusicBrainz `.tsv` tables into PostgreSQL using COPY for performance.
Includes chunked inserts, progress bars, and post-load row count verification.
"""

import os
import time
import pandas as pd
from io import StringIO
from tqdm import tqdm
import psycopg2
from config import (
    PG_HOST,
    PG_PORT,
    PG_DBNAME,
    PG_USER,
    PG_PASSWORD,
    MB_TSV_FILES
)

# --- Config ---
CHUNK_SIZE = 50_000
static_tables = [
    "artist",
    "artist_credit",
    "artist_credit_name",
    "release_group",
    "release_group_secondary_type",
    "release_group_secondary_type_join",
    "release",
]

# --- Connect to PostgreSQL ---
conn = psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    dbname=PG_DBNAME,
    user=PG_USER,
    password=PG_PASSWORD
)
cur = conn.cursor()

print("🔌 Connected to PostgreSQL")

for table in static_tables:
    file_path = MB_TSV_FILES.get(table)
    if not file_path or not os.path.exists(file_path):
        print(f"❌ Missing or invalid file for table '{table}': {file_path}")
        continue

    print(f"\n📅 Processing table: {table}")
    print(f"   ➔ Source: {file_path}")

    try:
        df = pd.read_csv(file_path, sep="\t", dtype=str, na_values="\\N", quoting=3, engine="python")
    except Exception as e:
        print(f"❌ Failed to read file: {e}")
        continue

    print(f"🧹 Dropping and recreating table '{table}'...")
    cur.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
    columns = [f'"{col}" TEXT' for col in df.columns]
    create_stmt = f'CREATE TABLE "{table}" ({", ".join(columns)});'
    cur.execute(create_stmt)
    conn.commit()

    print(f"🚀 Loading {len(df):,} rows into '{table}' using COPY...")
    start_time = time.time()

    for i in tqdm(range(0, len(df), CHUNK_SIZE), desc=f"🗃️ {table}", unit=" rows"):
        chunk = df.iloc[i:i + CHUNK_SIZE]
        buffer = StringIO()
        chunk.to_csv(buffer, sep="\t", header=False, index=False, na_rep='\\N')
        buffer.seek(0)

        try:
            cur.copy_expert(
                f'COPY "{table}" FROM STDIN WITH (FORMAT CSV, DELIMITER E\'\\t\', NULL \'\\N\')',
                buffer
            )
            conn.commit()
        except Exception as e:
            print(f"❌ COPY failed on chunk starting at row {i}: {e}")
            conn.rollback()
            break

    elapsed = time.time() - start_time
    print(f"⏱️ Load complete for '{table}' in {elapsed:.2f} seconds")

# --- Post-load Verification ---
print("\n🔍 Verifying row counts for all tables:")

for table in static_tables:
    try:
        cur.execute(f'SELECT COUNT(*) FROM "{table}";')
        count = cur.fetchone()[0]
        print(f"   • {table:<35} {count:,} rows")
    except Exception as e:
        print(f"❌ Could not count rows in {table}: {e}")

cur.close()
conn.close()
print("\n✅ Static MusicBrainz tables verified and loaded successfully.")
