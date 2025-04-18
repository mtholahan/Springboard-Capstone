'''
config.py

Centralized file path and API key config for Capstone project.
Update paths to match local dev environment. API key expected via environment.
'''

import os
from pathlib import Path

# === MusicBrainz File Paths ===
RAW_DIR = Path("D:/Capstone_Staging/data/musicbrainz_raw")
MB_FILES = {
    "artist": RAW_DIR / "artist",
    "artist_credit": RAW_DIR / "artist_credit",
    "artist_credit_name": RAW_DIR / "artist_credit_name",
    "release": RAW_DIR / "release",
    "release_group": RAW_DIR / "release_group",
    "release_group_secondary_type": RAW_DIR / "release_group_secondary_type",
    "release_group_secondary_type_join": RAW_DIR / "release_group_secondary_type_join",
}

# === Soundtrack Input and Processed Versions ===
MB_SOUNDTRACKS_FILE = RAW_DIR / "release_group_soundtracks.tsv"
MB_PARQUET_SOUNDTRACKS = RAW_DIR / "soundtracks.parquet"
JUNK_TITLE_LIST = RAW_DIR / "junk_mb_titles.txt"

# === TMDb Input and Output Files ===
TMDB_DIR = Path("D:/Capstone_Staging/data/tmdb")
TMDB_FILES = {
    "raw": TMDB_DIR / "tmdb_movie_raw.csv",
    "loose": TMDB_DIR / "tmdb_movie_loose.csv",
    "errors": TMDB_DIR / "tmdb_fetch_errors.txt",
    "no_results": TMDB_DIR / "tmdb_no_results.csv",
    "enriched_top_500": TMDB_DIR / "tmdb_top_500_enriched.csv",
    "enriched_top_1000": TMDB_DIR / "tmdb_top_1000_enriched.csv"
}

# === Top 500 Input CSV ===
TMDB_TOP_500_FILE = TMDB_DIR / "tmdb_top_500.csv"

# === Match Output Locations ===
MATCH_OUTPUTS = {
    "matched": TMDB_DIR / "tmdb_fuzzy_matches.tsv",
    "unmatched": TMDB_DIR / "tmdb_fuzzy_unmatched.tsv",
    "manual": TMDB_DIR / "manual_matches.csv"
}

# === TMDb API Key (expected via environment) ===
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
