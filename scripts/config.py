"""
Capstone Project Configuration File
Author: Mark
Last Updated: Sat, 20-April-2025

Defines constants for file paths, database connections, and refresh operations.
Organized by script number for clarity and maintainability.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import glob

# Load environment variables
load_dotenv()

# === Root Directories ===
BASE_DIR = Path("D:/Capstone_Staging")
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = DATA_DIR / "results"
TMDB_DIR = DATA_DIR / "tmdb"
MB_RAW_DIR = DATA_DIR / "musicbrainz_raw"

# === Script 00: MusicBrainz Dump Acquisition ===
MB_DUMP_ARCHIVE = BASE_DIR / "mbdump.tar.bz2"
MB_DUMP_DIR = BASE_DIR / "mbdump"

# === Script 02: TSV Cleanse ===
MB_TSV_FILES = {
    "artist": MB_RAW_DIR / "artist",
    "artist_credit": MB_RAW_DIR / "artist_credit",
    "artist_credit_name": MB_RAW_DIR / "artist_credit_name",
    "release": MB_RAW_DIR / "release",
    "release_group": MB_RAW_DIR / "release_group",
    "release_group_secondary_type": MB_RAW_DIR / "release_group_secondary_type",
    "release_group_secondary_type_join": MB_RAW_DIR / "release_group_secondary_type_join",
}

# === Script 05: Filtered Soundtracks ===
MB_PARQUET_SOUNDTRACKS = MB_RAW_DIR / "soundtracks.parquet"
MB_SECONDARY_TYPE_JOIN_FILE = MB_RAW_DIR / "release_group_secondary_type_join_clean.tsv"

# === Script 06: TMDb Movie Fetch ===
TOP_MOVIES_FILE = DATA_DIR / "top_movies_raw.csv"

# === Script 07–08: TMDb Enrichment ===
ENRICHED_FILE = TMDB_DIR / "enriched_top_1000.csv"

# === Script 09: Genre Normalization ===
TMDB_GENRE_FILE = TMDB_DIR / "tmdb_genre_top_1000.csv"
TMDB_MOVIE_GENRE_FILE = TMDB_DIR / "tmdb_movie_genre_top_1000.csv"

# === Script 10: Junk Title List ===
JUNK_TITLES_FILE = DATA_DIR / "junk_title_list.txt"

# === Script 11: Match Outputs ===
MATCHED_TSV = RESULTS_DIR / "matched_top_1000.tsv"
UNMATCHED_TSV = RESULTS_DIR / "unmatched_top_1000.tsv"

# Dynamically pick the latest diagnostics file
diagnostic_files = sorted(
    RESULTS_DIR.glob("matched_diagnostics_1000_*.tsv"),
    key=os.path.getmtime,
    reverse=True
)

if diagnostic_files:
    MATCHED_DIAGNOSTICS_TSV = diagnostic_files[0]
else:
    MATCHED_DIAGNOSTICS_TSV = None

MATCH_OUTPUTS = {
    "matched": MATCHED_TSV,
    "unmatched": UNMATCHED_TSV,
    "diagnostics": MATCHED_DIAGNOSTICS_TSV,
}

# === Script 13–15: PostgreSQL Settings ===
PG_HOST = "localhost"
PG_PORT = "5432"
PG_DBNAME = "musicbrainz"
PG_USER = "postgres"
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_SCHEMA = "public"

# === Script 13: Refresh Data Inputs ===
REFRESH_INPUTS = {
    "tmdb_movie": str(ENRICHED_FILE),
    "tmdb_genre": str(TMDB_GENRE_FILE),
    "tmdb_movie_genre": str(TMDB_MOVIE_GENRE_FILE),
    "soundtracks": str(MB_PARQUET_SOUNDTRACKS),
    "matched_top_1000": str(MATCHED_TSV),
    "unmatched_top_1000": str(UNMATCHED_TSV),
    "matched_diagnostics": str(MATCHED_DIAGNOSTICS_TSV),
}

# === Script 14: Refresh Static MusicBrainz Tables ===
MB_STATIC_REFRESH = {
    "artist": str(MB_TSV_FILES["artist"]),
    "artist_credit": str(MB_TSV_FILES["artist_credit"]),
    "artist_credit_name": str(MB_TSV_FILES["artist_credit_name"]),
    "release": str(MB_TSV_FILES["release"]),
    "release_group": str(MB_TSV_FILES["release_group"]),
    "release_group_secondary_type": str(MB_TSV_FILES["release_group_secondary_type"]),
    "release_group_secondary_type_join": str(MB_TSV_FILES["release_group_secondary_type_join"]),
}
