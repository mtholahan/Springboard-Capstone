# config.py

from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv

# === Load Environment Variables ===
load_dotenv()
PG_PASSWORD = os.getenv("PG_PASSWORD")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# === Shared Settings ===
BASE_DIR = Path("D:/Capstone_Staging")
DATA_DIR = BASE_DIR / "data"
TMDB_DIR = DATA_DIR / "tmdb"
MB_DIR = DATA_DIR / "musicbrainz_raw"
RESULTS_DIR = DATA_DIR / "results"
TOP_N = 1000
TODAY = datetime.now().strftime("%Y-%m-%d")

# === Script 06: Build Raw TMDb Input List ===
TOP_MOVIES_INPUT_FILE = TMDB_DIR / f"tmdb_top_movies_raw_{TOP_N}.csv"

# === Script 08: TMDb Metadata Enrichment ===
ENRICHED_FILE = TMDB_DIR / f"enriched_top_{TOP_N}.csv"

# === Script 09–10: Normalize TMDb Genres ===
TMDB_GENRE_FILE = TMDB_DIR / f"tmdb_genre_top_{TOP_N}.csv"
TMDB_MOVIE_GENRE_FILE = TMDB_DIR / f"tmdb_movie_genre_top_{TOP_N}.csv"

# === Script 11: Filter Soundtracks (MusicBrainz) ===
MB_PARQUET_SOUNDTRACKS = MB_DIR / "soundtracks.parquet"

# === Script 12: Match Soundtracks to TMDb ===
JUNK_TITLE_LIST = DATA_DIR / "junk_title_list.txt"
MANUAL_MATCH_FILE = RESULTS_DIR / "manual_rescue_matches.csv"
MATCHED_OUTPUT_FILE = RESULTS_DIR / f"matched_top_{TOP_N}.tsv"
UNMATCHED_OUTPUT_FILE = RESULTS_DIR / f"unmatched_top_{TOP_N}.tsv"
MATCH_DIAGNOSTIC_FILE = RESULTS_DIR / f"matched_diagnostics_{TOP_N}_{TODAY}.tsv"

# === Grouped Paths ===
TMDB_FILES = {
    "enriched_top_1000": ENRICHED_FILE,
    "genre_top_1000": TMDB_GENRE_FILE,
    "movie_genre_top_1000": TMDB_MOVIE_GENRE_FILE
}

MB_FILES = {
    "soundtracks": MB_PARQUET_SOUNDTRACKS
}

MATCH_OUTPUTS = {
    "matched": MATCHED_OUTPUT_FILE,
    "unmatched": UNMATCHED_OUTPUT_FILE,
    "diagnostics": MATCH_DIAGNOSTIC_FILE,
    "manual": MANUAL_MATCH_FILE
}

# === Script 13: PostgreSQL Refresh Inputs ===
REFRESH_INPUTS = {
    "tmdb_movie": str(ENRICHED_FILE),
    "tmdb_genre": str(TMDB_GENRE_FILE),
    "tmdb_movie_genre": str(TMDB_MOVIE_GENRE_FILE),
    "soundtracks": str(MB_PARQUET_SOUNDTRACKS),
    "matched_top_1000": str(MATCHED_OUTPUT_FILE),
    "unmatched_top_1000": str(UNMATCHED_OUTPUT_FILE),
    "matched_diagnostics": str(MATCH_DIAGNOSTIC_FILE)
}
