"""
07_tmdb_enrich_movies.py

Fetch full TMDb metadata and alternative titles for a list of movie IDs.
Source: Top 500 movies CSV. Output: Enriched movie details.
"""

import pandas as pd
import requests
import time
from config import TMDB_TOP_500_FILE, TMDB_FILES, TMDB_API_KEY

API_BASE = "https://api.themoviedb.org/3/movie"
INPUT_CSV = TMDB_TOP_500_FILE
OUTPUT_CSV = TMDB_FILES["enriched_top_500"]

sleep_time = 0.2

# --- LOAD INPUT ---
df = pd.read_csv(INPUT_CSV)
df = df.dropna(subset=["tmdb_id"])

records = []

for i, row in df.iterrows():
    tmdb_id = int(row["tmdb_id"])
    title = row["title"]
    print(f"[{i+1}/{len(df)}] Fetching TMDb ID {tmdb_id}: {title}")

    try:
        # Movie Details
        detail_url = f"{API_BASE}/{tmdb_id}"
        detail_params = {"api_key": TMDB_API_KEY}
        detail_resp = requests.get(detail_url, params=detail_params, timeout=10)
        detail_data = detail_resp.json()
        time.sleep(sleep_time)

        # Alternative Titles
        alt_url = f"{API_BASE}/{tmdb_id}/alternative_titles"
        alt_resp = requests.get(alt_url, params=detail_params, timeout=10)
        alt_data = alt_resp.json()
        time.sleep(sleep_time)

        alt_titles = [alt["title"] for alt in alt_data.get("titles", []) if "title" in alt]

        record = {
            "tmdb_id": tmdb_id,
            "title": title,
            "release_year": row.get("release_year"),
            "runtime": detail_data.get("runtime"),
            "genres": ", ".join([g["name"] for g in detail_data.get("genres", [])]),
            "overview": detail_data.get("overview"),
            "alt_titles": ", ".join(alt_titles),
        }
        records.append(record)

    except Exception as e:
        print(f"❌ Error fetching ID {tmdb_id}: {e}")

# --- SAVE ---
pd.DataFrame(records).to_csv(OUTPUT_CSV, index=False)
print(f"✅ Done. Saved enriched data to {OUTPUT_CSV}")
