"""
08_thdb_enrich_afi.py

Enriches AFI Top 100 movie titles with metadata from The Movie Database (TMDb).

- Sends each title to the TMDb Search API (with year parameter)
- Selects the best fuzzy match based on score minus year distance
- Retrieves popularity and genre(s) from search result
- Handles known title discrepancies using aliases
- Exports a CSV with enriched metadata for downstream use

Output:
- D:/Temp/mbdump/afi_enriched_tmdb.csv

Used in:
- match_05_fuzzy_afi_mb.py (for fuzzy linking to MusicBrainz)
"""

import pandas as pd
import requests
import time
from rapidfuzz import fuzz

# === CONFIG ===
API_KEY = "8289cf63ae0018475953afaf51ce5464"
SEARCH_URL = "https://api.themoviedb.org/3/search/multi"
GENRE_LIST_URL = "https://api.themoviedb.org/3/genre/{media_type}/list"
INPUT_CSV = "D:/Temp/mbdump/afi_top_100.csv"
OUTPUT_CSV = "D:/Temp/mbdump/afi_enriched_tmdb.csv"
THRESHOLD = 85
SLEEP_SECONDS = 0.3  # faster but still safe

# Optional alias correction for known TMDb title discrepancies
aliases = {
    "Dr. Strangelove": "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb"
}

# === FETCH GENRE MAPPINGS ===
def get_genre_lookup(media_type):
    r = requests.get(GENRE_LIST_URL.format(media_type=media_type), params={"api_key": API_KEY})
    if r.status_code == 200:
        return {g["id"]: g["name"] for g in r.json().get("genres", [])}
    return {}

movie_genres = get_genre_lookup("movie")
tv_genres = get_genre_lookup("tv")

# === SCORE FUNCTION ===
def score_result(result, title, target_year):
    name = result.get("title") or result.get("name") or ""
    alt_name = result.get("original_title") or ""
    score = max(
        fuzz.token_sort_ratio(title.lower(), name.lower()),
        fuzz.token_sort_ratio(title.lower(), alt_name.lower())
    )
    year_str = result.get("release_date") or result.get("first_air_date")
    year_val = int(year_str[:4]) if year_str and year_str[:4].isdigit() else None
    year_diff = abs(int(target_year) - year_val) if year_val else 99
    return score - year_diff, score

# === LOAD ===
movies = pd.read_csv(INPUT_CSV)
results = []

# === TMDb QUERY LOOP ===
for i, row in movies.iterrows():
    raw_title = row["title"]
    year = str(row["year"])
    title = aliases.get(raw_title, raw_title)

    params = {
        "api_key": API_KEY,
        "query": title,
        "include_adult": False,
        "year": year
    }

    print(f"[{i+1}] 🎬 Searching: {raw_title} ({year})")
    r = requests.get(SEARCH_URL, params=params)
    if r.status_code != 200:
        print(f"   ❌ HTTP Error {r.status_code}")
        continue

    best_result = None
    best_final_score = 0
    best_raw_score = 0
    for result in r.json().get("results", []):
        final_score, raw_score = score_result(result, title, year)
        if final_score > best_final_score:
            best_result = result
            best_final_score = final_score
            best_raw_score = raw_score

    if best_result and best_raw_score >= THRESHOLD:
        media_type = best_result.get("media_type")
        genre_ids = best_result.get("genre_ids", [])
        genre_lookup = movie_genres if media_type == "movie" else tv_genres
        genre_names = [genre_lookup.get(gid, "") for gid in genre_ids if gid in genre_lookup]

        results.append({
            "input_title": raw_title,
            "input_year": year,
            "tmdb_title": best_result.get("title") or best_result.get("name"),
            "tmdb_year": best_result.get("release_date") or best_result.get("first_air_date"),
            "media_type": media_type,
            "tmdb_id": best_result.get("id"),
            "popularity": best_result.get("popularity"),
            "fuzzy_score": best_raw_score,
            "genres": ", ".join(genre_names) if genre_names else "Unknown"
        })

        print(f"   ✅ Match: {best_result.get('title') or best_result.get('name')} ({best_raw_score}%)")
    else:
        results.append({
            "input_title": raw_title,
            "input_year": year,
            "tmdb_title": None,
            "tmdb_year": None,
            "media_type": None,
            "popularity": None,
            "fuzzy_score": best_raw_score,
            "genres": None
        })
        print(f"   ❌ No strong match (score: {best_raw_score}%)")

    time.sleep(SLEEP_SECONDS)

# === EXPORT ===
df_results = pd.DataFrame(results)
df_results.to_csv(OUTPUT_CSV, index=False)
print(f"\n✅ Enrichment complete. Output saved to '{OUTPUT_CSV}'")
