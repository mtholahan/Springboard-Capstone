"""
13_tmdb_tables_refresh.py

This script recreates and loads the main analysis-ready tables into the 'musicbrainz' PostgreSQL database.
It handles enriched TMDb data, the filtered MusicBrainz soundtracks, and final matching results from the 
fuzzy linking process.

Foreign key-sensitive table order is preserved.

Sources include:
- CSVs for enriched movies, genre data, and movie-genre links
- Parquet for MusicBrainz soundtracks
- TSVs for match outputs from the fuzzy pipeline

"""

import pandas as pd
from sqlalchemy import create_engine, text
from config import (
    PG_HOST,
    PG_PORT,
    PG_DBNAME,
    PG_USER,
    PG_PASSWORD,
    ENRICHED_FILE,
    TMDB_GENRE_FILE,
    TMDB_MOVIE_GENRE_FILE,
    MB_PARQUET_SOUNDTRACKS,
    MATCH_OUTPUTS
)

# --- Build the PostgreSQL connection string ---
DB_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}"
engine = create_engine(DB_URL)

# Map table names to files (order matters for FK constraints)
REFRESH_INPUTS = {
    "tmdb_movie_genre": str(TMDB_MOVIE_GENRE_FILE),
    "tmdb_genre": str(TMDB_GENRE_FILE),
    "tmdb_movie": str(ENRICHED_FILE),
    "soundtracks": str(MB_PARQUET_SOUNDTRACKS),
    "matched_top_1000": str(MATCH_OUTPUTS["matched"]),
    "unmatched_top_1000": str(MATCH_OUTPUTS["unmatched"]),
    "matched_diagnostics": str(MATCH_OUTPUTS["diagnostics"])
}

print("🔌 Connecting to PostgreSQL...\n")

with engine.begin() as conn:
    for table, file in REFRESH_INPUTS.items():
        print(f"📅 Processing file for table: {table}")
        print(f"   ➤ {file}")

        # Load the file
        if file.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.endswith(".tsv"):
            df = pd.read_csv(file, sep="\t")
        elif file.endswith(".parquet"):
            df = pd.read_parquet(file)
        else:
            print(f"❌ Unsupported file format: {file}")
            continue

        # Recreate the table
        print(f"🧹 Dropping and recreating table {table}...")
        conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE;"))

        columns = [f'"{col}" {"TEXT" if df[col].dtype == object else "INTEGER"}' for col in df.columns]
        create_stmt = f"""
        CREATE TABLE {table} (
            {', '.join(columns)}
        );
        """
        conn.execute(text(create_stmt))

        print(f"📄 Inserting {len(df):,} rows into {table} ...")
        df.to_sql(table, con=conn, if_exists="append", index=False, method="multi")

print("✅ TMDb tables refreshed.")
