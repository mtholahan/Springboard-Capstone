"""
06_build_top_movies_raw.py

Fetches the top N TMDb movies based on popularity or rating.
Creates the raw input file used in downstream enrichment:
  -> data/tmdb/tmdb_top_movies_raw_{TOP_N}.csv

Columns: tmdb_id, title, release_year
"""

import requests
import pandas as pd
import time
from config import TOP_N, TMDB_API_KEY, TOP_MOVIES_INPUT_FILE

API_BASE = "https://api.themoviedb.org/3/movie/top_rated"
MOVIES_PER_PAGE = 20
TOTAL_PAGES = (TOP_N + MOVIES_PER_PAGE - 1) // MOVIES_PER_PAGE

params = {
    "api_key": TMDB_API_KEY,
    "language": "en-US",
    "page": 1
}

movies = []
TOP_MOVIES_INPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

print(f"📥 Fetching top {TOP_N} movies from TMDb...")

for page in range(1, TOTAL_PAGES + 1):
    params["page"] = page
    try:
        response = requests.get(API_BASE, params=params, timeout=10)
        data = response.json()
        results = data.get("results", [])

        for movie in results:
            movies.append({
                "tmdb_id": movie["id"],
                "title": movie["title"],
                "release_year": movie.get("release_date", "")[:4]
            })

        print(f"✅ Page {page} fetched ({len(results)} movies)")
        time.sleep(0.2)

        if len(movies) >= TOP_N:
            break

    except Exception as e:
        print(f"❌ Error fetching page {page}: {e}")
        break

# --- Trim and Save ---
df = pd.DataFrame(movies[:TOP_N])
df.to_csv(TOP_MOVIES_INPUT_FILE, index=False)
print(f"✅ Saved top {len(df)} movies to {TOP_MOVIES_INPUT_FILE}")
