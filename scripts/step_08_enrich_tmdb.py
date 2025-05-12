import pandas as pd
import requests
import time
from tqdm import tqdm
from config import TMDB_API_KEY
from pathlib import Path

# --- Config ---
INPUT_MATCHES = Path("D:/Capstone_Staging/data/tmdb/tmdb_match_results.csv")
OUTPUT_FILE = Path("D:/Capstone_Staging/data/tmdb/tmdb_enriched_matches.csv")
TMDB_API_BASE = "https://api.themoviedb.org/3/movie"
SLEEP_TIME = 0.25  # ~4 requests/sec to respect TMDb limits

def clean(text):
    """Ensure UTF-8 encoding and remove problematic characters."""
    if pd.isna(text):
        return ""
    return str(text).encode("latin1", errors="ignore").decode("utf-8", errors="ignore").strip()

def main():
    print("📥 Loading matches from Step 07...")
    matches = pd.read_csv(INPUT_MATCHES)

    enriched = []

    print("🎯 Enriching matches...")
    for _, row in tqdm(matches.iterrows(), total=len(matches), desc="🎯 Enriching matches"):
        tmdb_id = row["tmdb_id"]

        result = {
            "tmdb_id": tmdb_id,
            "tmdb_title": clean(row["tmdb_title"]),
            "matched_title": clean(row["matched_title"]),
            "release_year": row["release_year"],
            "score": row["score"],
            "release_group_id": row["release_group_id"],
            "runtime": None,
            "genres": "",
            "overview": "",
            "alt_titles": ""
        }

        # Fetch movie details
        try:
            resp = requests.get(f"{TMDB_API_BASE}/{tmdb_id}", params={"api_key": TMDB_API_KEY}, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            result["runtime"] = data.get("runtime")
            result["genres"] = ", ".join([g["name"] for g in data.get("genres", [])])
            result["overview"] = clean(data.get("overview", ""))
            time.sleep(SLEEP_TIME)

        except requests.exceptions.HTTPError as e:
            print(f"❌ Error fetching movie details for {tmdb_id}: {e}")
            continue

        # Fetch alternative titles
        try:
            alt_resp = requests.get(f"{TMDB_API_BASE}/{tmdb_id}/alternative_titles", params={"api_key": TMDB_API_KEY}, timeout=10)
            alt_resp.raise_for_status()
            alt_data = alt_resp.json()
            alt_titles = [clean(alt["title"]) for alt in alt_data.get("titles", []) if "title" in alt]
            result["alt_titles"] = ", ".join(alt_titles)
            time.sleep(SLEEP_TIME)

        except requests.exceptions.HTTPError as e:
            print(f"❌ Error fetching alt titles for {tmdb_id}: {e}")

        enriched.append(result)

    df = pd.DataFrame(enriched)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    print(f"✅ Done. Saved {len(df)} enriched results to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
