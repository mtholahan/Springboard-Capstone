"""
06_tmdb_fetch_movies_ready.py (FINALIZED FIX)
Guarantees that tmdb_no_results.csv is written for true zero-score or unaccepted matches.
"""

import pandas as pd
import requests
import os
import argparse
from time import sleep
from rapidfuzz import fuzz
from _99_util_clean_title import clean_title
from config import MB_SOUNDTRACKS_FILE, TMDB_FILES

# --- ARGPARSE ---
parser = argparse.ArgumentParser(description="Match MusicBrainz titles to TMDb using fuzzy logic")
parser.add_argument("--limit", type=int, default=None, help="Optional limit on number of rows to process")
args = parser.parse_args()

# --- CONFIG ---
AUDIT_LOG = []
RESCUE_MAP = {
    "outpost": 16548,
    "lost and gone forever": 68212,
    "ghosts of dead aeroplanes": 24654,
    "mr robot volume 4": 62560,
    "max payne 2": 41799,
    "rayman origins": 10437,
    "alien isolation": 228161,
    "ghostbusters ii": 620,
    "lost horizon": 23460,
    "hellraiser": 10849
}
INPUT_PATH = MB_SOUNDTRACKS_FILE
OUTPUT_STRONG = TMDB_FILES["raw"]
OUTPUT_WEAK = TMDB_FILES["loose"]
OUTPUT_ERROR = TMDB_FILES["errors"]
OUTPUT_ZERO_HITS = TMDB_FILES.get("no_results", "tmdb_no_results.csv")
FUZZY_THRESHOLD = 85
COMPOSITE_THRESHOLD = 90
YEAR_WINDOW = 2
API_SLEEP = 0.25
MAX_RESULTS = 5
ENABLE_ALT_TITLES = True

# --- TMDB SEARCH ---
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def tmdb_search(query):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": query, "include_adult": False}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("results", [])

def fetch_tmdb_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def fetch_alternative_titles(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/alternative_titles"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return [alt['title'] for alt in data.get("titles", []) if 'title' in alt]

# --- CLEANING HELPERS ---
STOPWORDS_SKIP = ["2005", "post", "volume", "deluxe", "soundtrack album", "special edition"]
TITLE_BLACKLIST = [
    "original soundtrack", "soundtrack album", "music from", "tv series",
    "volume", "score", "complete motion picture soundtrack", "remastered",
    "deluxe", "anniversary", "special edition", "expanded edition"
]

def should_skip_title(title):
    clean = title.lower().strip()
    if len(clean.split()) < 3:
        for word in STOPWORDS_SKIP:
            if word in clean:
                return True
    return False

def strip_blacklisted_phrases(title):
    title = title.lower()
    for phrase in TITLE_BLACKLIST:
        title = title.replace(phrase, "")
    return " ".join(title.split())

# --- LOAD DATA ---
df = pd.read_csv(INPUT_PATH, sep='\t', encoding='utf-8')
df["cleaned_title"] = df["name_x"].apply(clean_title)
df["mb_soundtrack_title"] = df["name_x"]
if args.limit:
    df = df.head(args.limit)

# --- MAIN LOOP ---
rows_strong, rows_weak, errors, rows_zero = [], [], [], []

for i, row in df.iterrows():
    if should_skip_title(row["name_x"]):
        errors.append(f"{row['name_x']} | Skipped due to stopword rule")
        continue

    mb_title = row["mb_soundtrack_title"]
    cleaned = row["cleaned_title"]
    mb_year = row.get("mb_year")
    best_score, best_match = 0, None
    reasons = []

    if i % 50 == 0:
        print(f"[{i}/{len(df)}] Querying TMDb for: {cleaned}")

    try:
        # --- RESCUE OVERRIDE ---
        if cleaned in RESCUE_MAP:
            tmdb_id = RESCUE_MAP[cleaned]
            print(f"    RESCUE: Using TMDb ID {tmdb_id} for {cleaned}")
            movie_details = fetch_tmdb_movie_details(tmdb_id)
            alt_titles = fetch_alternative_titles(tmdb_id) if ENABLE_ALT_TITLES else []
            result = movie_details.copy()
            result.update({
                "mb_soundtrack_title": mb_title,
                "tmdb_query_used": cleaned,
                "composite_score": 100,
                "match_reasons": "rescue_override"
            })
            rows_strong.append(result)
            continue

        results = tmdb_search(cleaned)
        sleep(API_SLEEP)

        if not results:
            rows_zero.append({"mb_title": mb_title, "query": cleaned})
            continue

        for result in results[:MAX_RESULTS]:
            title = result.get("title", "")
            fuzzy_score = fuzz.token_sort_ratio(cleaned, title.lower())
            substring_hit = cleaned in title.lower()
            tmdb_id = result.get("id")
            movie_details = fetch_tmdb_movie_details(tmdb_id)

            genres = [g['name'].lower() for g in movie_details.get("genres", [])]
            runtime = movie_details.get("runtime") or 0
            overview = (movie_details.get("overview") or "").lower()

            if runtime < 20 or any(term in genres for term in ["documentary", "tv movie", "short"]):
                continue

            composite_score = fuzzy_score
            reasons = [f"fuzzy:{fuzzy_score}"]
            if substring_hit:
                composite_score += 10
                reasons.append("substring")
            if any(term in genres for term in ["action", "drama", "music"]):
                composite_score += 5
                reasons.append("genre_bonus")
            if any(keyword in overview for keyword in ["video game", "series", "live performance"]):
                composite_score -= 5
                reasons.append("overview_penalty")

            if composite_score > best_score:
                best_score = composite_score
                best_match = result.copy()
                best_match.update({
                    "mb_soundtrack_title": mb_title,
                    "tmdb_query_used": cleaned,
                    "composite_score": composite_score,
                    "match_reasons": ", ".join(reasons)
                })

        if best_match:
            AUDIT_LOG.append({
                "mb_title": mb_title,
                "tmdb_title": best_match.get("title"),
                "score": best_score,
                "reasons": reasons,
                "final_decision": "strong" if best_score >= COMPOSITE_THRESHOLD else "loose"
            })
            if best_score >= COMPOSITE_THRESHOLD:
                rows_strong.append(best_match)
            else:
                rows_weak.append(best_match)
        else:
            errors.append(f"{mb_title} | No good match above threshold (best_score={best_score})")
            rows_zero.append({"mb_title": mb_title, "query": cleaned})

    except Exception as e:
        print(f"ERROR on row {i}: {e}")
        errors.append(f"{mb_title} | ERROR: {e}")
        rows_zero.append({"mb_title": mb_title, "query": cleaned})

# --- OUTPUTS ---
pd.DataFrame(rows_strong).to_csv(OUTPUT_STRONG, index=False)
pd.DataFrame(rows_weak).to_csv(OUTPUT_WEAK, index=False)
pd.DataFrame(rows_zero).to_csv(OUTPUT_ZERO_HITS, index=False)  # ALWAYS written

with open(OUTPUT_ERROR, "w", encoding="utf-8") as f:
    f.write("\n".join(errors))

try:
    pd.DataFrame(AUDIT_LOG).to_csv("tmdb_match_audit.csv", index=False)
except Exception as e:
    print(f"Audit log write failed: {e}")

print(f"\nDone. Strong matches: {len(rows_strong)} | Loose: {len(rows_weak)} | Zero-hits: {len(rows_zero)} | Errors: {len(errors)}")
