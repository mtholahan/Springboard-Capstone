"""
08_tmdb_enrich_alt_titles.py

Fetch full TMDb metadata and alternative titles for the Top N movie list.
Enhances and overwrites enriched_top_{TOP_N}.csv with alt titles, runtime, overview, genres.
Filters out alt titles with known mojibake/junk patterns.
"""

import pandas as pd
import requests
import time
from config import ENRICHED_FILE, TMDB_API_KEY

API_BASE = "https://api.themoviedb.org/3/movie"
sleep_time = 0.3

# --- LOAD INPUT ---
df = pd.read_csv(ENRICHED_FILE)
df = df.dropna(subset=["tmdb_id"])

# --- Helper to detect mojibake ---
def is_clean(text):
    junk_fragments = ['ã€', 'Ã', 'â€™', 'â€“', 'â€œ', 'â€']
    return not any(fragment in text for fragment in junk_fragments)

records = []

for i, row in df.iterrows():
    tmdb_id = int(row["tmdb_id"])
    title = row["title"]
    print(f"[{i+1}/{len(df)}] Enriching TMDb ID {tmdb_id}: {title}")

    try:
        detail_url = f"{API_BASE}/{tmdb_id}"
        detail_params = {"api_key": TMDB_API_KEY}
        detail_resp = requests.get(detail_url, params=detail_params, timeout=10)
        detail_data = detail_resp.json()
        time.sleep(sleep_time)

        alt_url = f"{API_BASE}/{tmdb_id}/alternative_titles"
        alt_resp = requests.get(alt_url, params=detail_params, timeout=10)
        alt_data = alt_resp.json()
        time.sleep(sleep_time)

        alt_titles = [alt.get("title", "") for alt in alt_data.get("titles", []) if is_clean(alt.get("title", ""))]

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
        print(f"❌ Error with ID {tmdb_id}: {e}")

# --- SAVE ---
pd.DataFrame(records).to_csv(ENRICHED_FILE, index=False, encoding="utf-8")
print(f"✅ Done. Enriched metadata saved to {ENRICHED_FILE}")
