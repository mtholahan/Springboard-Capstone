"""
config.py

Centralized file path and API key config for Capstone project.
Update paths to match local dev environment. API key expected via environment.
"""

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

# === Soundtrack Input ===
MB_SOUNDTRACKS_FILE = RAW_DIR / "release_group_soundtracks.tsv"

# === TMDb Output Files ===
TMDB_DIR = Path("D:/Capstone_Staging/data/tmdb")
TMDB_FILES = {
    "raw": TMDB_DIR / "tmdb_movie_raw.csv",
    "loose": TMDB_DIR / "tmdb_movie_loose.csv",
    "errors": TMDB_DIR / "tmdb_fetch_errors.txt",
}

# === TMDb API Key (expected via environment) ===
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
