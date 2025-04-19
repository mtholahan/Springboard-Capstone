# config.py

from pathlib import Path
from datetime import datetime
import os

# --- Base Directory ---
BASE_DIR = Path("D:/Capstone_Staging")

# --- Script 06: Build Raw TMDb Input List ---
TOP_N = 1000  # Change this to dynamically set your input size
TOP_MOVIES_INPUT_FILE = BASE_DIR / "data" / "tmdb" / f"tmdb_top_movies_raw_{TOP_N}.csv"  # Input list of TMDb IDs

# --- Script 07: Fetch TMDb Metadata ---
TMDB_API_KEY = os.getenv("TMDB_API_KEY")  # Set this in your system environment variables

# --- Script 08: Enrich TMDb Metadata ---
ENRICHED_FILE = BASE_DIR / "data" / "tmdb" / f"enriched_top_{TOP_N}.csv"  # Combined metadata

# --- Script 09: Enrich TMDb Alt Titles & Runtime ---
# Uses enriched file, overwrites/enhances missing details

# --- Script 10: Normalize Genres ---
TMDB_GENRE_FILE = BASE_DIR / "data" / "tmdb" / f"tmdb_genre_top_{TOP_N}.csv"  # Genre dimension
TMDB_MOVIE_GENRE_FILE = BASE_DIR / "data" / "tmdb" / f"tmdb_movie_genre_top_{TOP_N}.csv"  # Genre link table

# --- Script 11: Soundtrack Inputs ---
MB_PARQUET_SOUNDTRACKS = BASE_DIR / "data" / "musicbrainz_raw" / "soundtracks.parquet"

# --- Script 12: Fuzzy Match Support ---
JUNK_TITLE_LIST = BASE_DIR / "data" / "junk_title_list.txt"
MATCH_OUTPUT_DIR = BASE_DIR / "results"
MATCHED_OUTPUT_FILE = MATCH_OUTPUT_DIR / f"matched_top_{TOP_N}.tsv"
UNMATCHED_OUTPUT_FILE = MATCH_OUTPUT_DIR / f"unmatched_top_{TOP_N}.tsv"
MANUAL_MATCH_FILE = MATCH_OUTPUT_DIR / "manual_rescue_matches.csv"

# --- Dynamic diagnostics output ---
TODAY = datetime.now().strftime("%Y-%m-%d")
MATCH_DIAGNOSTIC_FILE = MATCH_OUTPUT_DIR / f"matched_diagnostics_{TOP_N}_{TODAY}.tsv"
