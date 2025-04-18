"""
10_match_fuzzy_link_soundtracks.py

Fuzzy-matching MusicBrainz soundtrack titles to TMDb enriched metadata.
Supports manual rescue map and junk filtering. Writes match results to tsv.
"""

import pandas as pd
import numpy as np
from rapidfuzz import fuzz
from config import (
    MB_PARQUET_SOUNDTRACKS,
    TMDB_FILES,
    MATCH_OUTPUTS,
    JUNK_TITLE_LIST
)

# --- PARAMETERS ---
FUZZ_THRESHOLD = 85
MAX_RESULTS = 1
ENABLE_SUBSTRING_MATCH = True

# --- LOAD DATA ---
mb = pd.read_parquet(MB_PARQUET_SOUNDTRACKS)
tmdb = pd.read_csv(TMDB_FILES["enriched_top_1000"])

junk_titles = set()
with open(JUNK_TITLE_LIST, encoding="utf-8") as f:
    for line in f:
        junk_titles.add(line.strip().lower())

manual_df = pd.read_csv(MATCH_OUTPUTS["manual"]) if MATCH_OUTPUTS["manual"].exists() else pd.DataFrame()
manual_lookup = dict(zip(manual_df["mb_title"].str.lower(), manual_df["tmdb_id"]))

# --- MATCH LOGIC ---
matched, unmatched = [], []

def clean_title(t):
    return str(t).lower().strip()

for idx, row in mb.iterrows():
    mb_title = clean_title(row["name_x"])

    if mb_title in junk_titles:
        continue

    if mb_title in manual_lookup:
        tmdb_id = manual_lookup[mb_title]
        match_row = tmdb[tmdb["id"] == tmdb_id]
        if not match_row.empty:
            result = row.to_dict()
            result.update({"tmdb_id": tmdb_id, "match_score": 100, "match_method": "manual"})
            matched.append(result)
        continue

    best_score, best_id = 0, None
    for _, tmdb_row in tmdb.iterrows():
        tmdb_title = clean_title(tmdb_row["title"])
        score = fuzz.token_sort_ratio(mb_title, tmdb_title)
        if ENABLE_SUBSTRING_MATCH and mb_title in tmdb_title:
            score += 10
        if score > best_score:
            best_score = score
            best_id = tmdb_row["id"]

    if best_score >= FUZZ_THRESHOLD:
        result = row.to_dict()
        result.update({"tmdb_id": best_id, "match_score": best_score, "match_method": "fuzzy"})
        matched.append(result)
    else:
        unmatched.append(row)

# --- SAVE OUTPUT ---
pd.DataFrame(matched).to_csv(MATCH_OUTPUTS["matched"], sep="\t", index=False)
pd.DataFrame(unmatched).to_csv(MATCH_OUTPUTS["unmatched"], sep="\t", index=False)
print(f"✅ Done. Matches: {len(matched)} | Unmatched: {len(unmatched)}")
