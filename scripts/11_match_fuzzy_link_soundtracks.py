"""
11_match_fuzzy_link_soundtracks.py

Performs fuzzy matching between MusicBrainz soundtrack titles and TMDb enriched movie list.
Generates match results and saves matched/unmatched TSVs in the results/ folder.
Supports optional manual rescue match file: manual_rescue_matches.csv
Uses rapidfuzz for token-based fuzzy matching.
"""

import pandas as pd
import os
import time
from pathlib import Path
from config import (
    MB_PARQUET_SOUNDTRACKS,
    ENRICHED_FILE,
    MATCH_OUTPUT_DIR,
    MATCHED_OUTPUT_FILE,
    UNMATCHED_OUTPUT_FILE,
    MANUAL_MATCH_FILE,
    MATCH_DIAGNOSTIC_FILE
)
from rapidfuzz import fuzz

# --- Ensure results directory exists ---
Path(MATCH_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# --- Load datasets ---
mb = pd.read_parquet(MB_PARQUET_SOUNDTRACKS)
tmdb = pd.read_csv(ENRICHED_FILE)

# --- Load manual matches if available ---
if Path(MANUAL_MATCH_FILE).exists():
    manual_df = pd.read_csv(MANUAL_MATCH_FILE)
    if "mb_title" in manual_df.columns and "tmdb_id" in manual_df.columns:
        manual_lookup = dict(zip(manual_df["mb_title"].str.lower(), manual_df["tmdb_id"]))
        print(f"✅ Loaded {len(manual_lookup)} manual rescue entries")
    else:
        manual_lookup = {}
        print("⚠️ manual_rescue_matches.csv is missing expected columns — skipping")
else:
    manual_lookup = {}
    print("ℹ️ No manual rescue file found. Skipping manual overrides.")

# --- Fuzzy match logic ---
matched = []
unmatched = []
diagnostics = []

for i, row in mb.iterrows():
    mb_title = row["name"]  # updated to reflect actual column name
    mb_title_lc = mb_title.lower()

    if i % 50 == 0 or i == len(mb) - 1:
        print(f"🔍 [{i+1}/{len(mb)}] Matching: \"{mb_title[:40]}\"...")

    # Manual override?
    if mb_title_lc in manual_lookup:
        matched.append({"mb_title": mb_title, "tmdb_id": manual_lookup[mb_title_lc], "score": 100, "method": "manual"})
        continue

    best_score = 0
    best_match = None

    for j, tmdb_row in tmdb.iterrows():
        tmdb_title = tmdb_row["title"]
        score = fuzz.token_sort_ratio(mb_title, tmdb_title)
        if score > best_score:
            best_score = score
            best_match = tmdb_row

    diagnostics.append({"mb_title": mb_title, "tmdb_guess": best_match["title"] if best_match is not None else None, "score": best_score})

    if best_score >= 90:
        matched.append({"mb_title": mb_title, "tmdb_id": best_match["tmdb_id"], "score": best_score, "method": "fuzzy"})
    else:
        unmatched.append({"mb_title": mb_title, "score": best_score})

# --- Save results ---
pd.DataFrame(matched).to_csv(MATCHED_OUTPUT_FILE, sep="\t", index=False)
pd.DataFrame(unmatched).to_csv(UNMATCHED_OUTPUT_FILE, sep="\t", index=False)
pd.DataFrame(diagnostics).to_csv(MATCH_DIAGNOSTIC_FILE, sep="\t", index=False)

print(f"✅ Matching complete: {len(matched)} matched, {len(unmatched)} unmatched")
