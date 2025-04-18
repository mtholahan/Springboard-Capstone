"""
06_tmdb_fetch_movies_ready.py

Match MusicBrainz soundtrack titles to TMDb using fuzzy search and rescue logic.
Supports a junk title list loaded from file.
"""

import pandas as pd
import requests
import time
from difflib import SequenceMatcher
from config import (
    MB_SOUNDTRACKS_FILE,
    TMDB_FILES,
    TMDB_API_KEY,
    JUNK_TITLE_LIST
)

# --- Load junk/problematic titles ---
def load_problem_titles():
    with open(JUNK_TITLE_LIST, encoding="utf-8") as f:
        return set(line.strip().lower() for line in f if line.strip())

PROBLEM_TITLES = load_problem_titles()

# --- Load soundtracks ---
mb = pd.read_csv(MB_SOUNDTRACKS_FILE, sep='\t')

# --- CLI args ---
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--limit", type=int, default=len(mb))
parser.add_argument("--results", type=int, default=5)
args = parser.parse_args()

# --- Helper ---
def clean(title):
    return title.lower().strip()

def tmdb_search(query):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": query}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json().get("results", [])

# --- Main loop ---
raw_matches, loose_matches, errors, no_results = [], [], [], []

for i, row in mb.head(args.limit).iterrows():
    original = row["name"]
    cleaned = clean(original)
    print(f"\n=== [{i}/{args.limit}] Processing: {original} ===")

    if cleaned in PROBLEM_TITLES:
        print(f"    ⏭️ Skipping known problematic query: {cleaned}")
        continue

    print(f"    → Sending search query to TMDb: {cleaned}")
    try:
        results = tmdb_search(cleaned)
        print(f"    ← Search response received")

        if not results:
            no_results.append(original)
            continue

        top_n = results[:args.results]
        best_score = 0
        best = None

        for r in top_n:
            ratio = SequenceMatcher(None, cleaned, clean(r["title"])).ratio()
            score = ratio * 100
            if score > best_score:
                best_score = score
                best = r

        if best_score >= 90:
            raw_matches.append({"mb_title": original, "tmdb_id": best["id"], "score": round(best_score, 1)})
            print(f"    ✅ Best match score: {best_score:.1f} — strong")
        else:
            loose_matches.append({"mb_title": original, "candidates": len(results), "best_score": round(best_score, 1)})
            print(f"    ❔ No match above threshold")

        time.sleep(0.25)

    except Exception as e:
        print(f"    ❌ TMDb query error: {e}")
        errors.append(original)

# --- Save results ---
pd.DataFrame(raw_matches).to_csv(TMDB_FILES["raw"], index=False)
pd.DataFrame(loose_matches).to_csv(TMDB_FILES["loose"], index=False)
pd.DataFrame(no_results).to_csv(TMDB_FILES["no_results"], index=False)
with open(TMDB_FILES["errors"], "w", encoding="utf-8") as f:
    for title in errors:
        f.write(title + "\n")

print("\nDone.")
print(f"Strong matches: {len(raw_matches)} | Loose: {len(loose_matches)} | Zero-hits: {len(no_results)} | Errors: {len(errors)}")
