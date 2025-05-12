"""
Capstone Project Configuration File
Author: Mark
Last Updated: Thu, 08-May-2025

Defines constants for file paths, filenames, and database settings used throughout the ETL pipeline.
Organized by logical grouping: paths, MusicBrainz data, TMDb data, output files, and Postgres.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (used for DB password)
load_dotenv()

# === Base Paths ===
BASE_DIR = Path("D:/Capstone_Staging")
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = DATA_DIR / "results"
TMDB_DIR = DATA_DIR / "tmdb"
MB_RAW_DIR = DATA_DIR / "musicbrainz_raw"
MB_CLEANSED_DIR = MB_RAW_DIR / "cleansed"
SEVEN_ZIP_PATH = Path("C:/Program Files/7-Zip/7z.exe")

# === Whitelist of MusicBrainz TSV File Names (no extensions) ===
TSV_WHITELIST = {
    "artist", "artist_credit", "artist_credit_name", "release",
    "release_group", "release_group_secondary_type", "release_group_secondary_type_join"
}

# === MusicBrainz File Mappings ===
MB_RAW_FILES = {name: MB_RAW_DIR / name for name in TSV_WHITELIST}
MB_TSV_FILES = {name: MB_CLEANSED_DIR / name for name in TSV_WHITELIST}

# === MusicBrainz Archive Inputs ===
MB_DUMP_ARCHIVE = BASE_DIR / "mbdump.tar.bz2"
MB_DUMP_DIR = BASE_DIR / "mbdump"
MB_PARQUET_SOUNDTRACKS = MB_RAW_DIR / "soundtracks.parquet"
MB_SECONDARY_TYPE_JOIN_FILE = MB_RAW_DIR / "release_group_secondary_type_join_clean.tsv"

# === TMDB API Key ===
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# === TMDb Data Inputs ===
TOP_MOVIES_FILE = DATA_DIR / "top_movies_raw.csv"
ENRICHED_FILE = TMDB_DIR / "enriched_top_1000.csv"
TMDB_GENRE_FILE = TMDB_DIR / "tmdb_genre_top_1000.csv"
TMDB_MOVIE_GENRE_FILE = TMDB_DIR / "tmdb_movie_genre_top_1000.csv"
JUNK_TITLES_FILE = DATA_DIR / "junk_title_list.txt"

# === Match Output Files ===
MATCHED_TSV = RESULTS_DIR / "matched_top_1000.tsv"
UNMATCHED_TSV = RESULTS_DIR / "unmatched_top_1000.tsv"
diagnostic_files = sorted(RESULTS_DIR.glob("matched_diagnostics_1000_*.tsv"), key=os.path.getmtime, reverse=True)
MATCHED_DIAGNOSTICS_TSV = diagnostic_files[0] if diagnostic_files else None

MATCH_OUTPUTS = {
    "matched": MATCHED_TSV,
    "unmatched": UNMATCHED_TSV,
    "diagnostics": MATCHED_DIAGNOSTICS_TSV,
}

# === PostgreSQL Database Settings ===
PG_HOST = "localhost"
PG_PORT = "5432"
PG_DBNAME = "musicbrainz"
PG_USER = "postgres"
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_SCHEMA = "public"

# === Input Refresh Map for Step 13 ===
REFRESH_INPUTS = {
    "tmdb_movie": str(ENRICHED_FILE),
    "tmdb_genre": str(TMDB_GENRE_FILE),
    "tmdb_movie_genre": str(TMDB_MOVIE_GENRE_FILE),
    "soundtracks": str(MB_PARQUET_SOUNDTRACKS),
    "matched_top_1000": str(MATCHED_TSV),
    "unmatched_top_1000": str(UNMATCHED_TSV),
    "matched_diagnostics": str(MATCHED_DIAGNOSTICS_TSV),
}

# === Static Table Refresh Map for Step 14 ===
MB_STATIC_REFRESH = {
    name: str(MB_TSV_FILES[name]) for name in TSV_WHITELIST
}
