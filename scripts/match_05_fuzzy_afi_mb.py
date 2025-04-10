"""
match_05_fuzzy_afi_mb.py

Fuzzy matches TMDb-enriched AFI titles against MusicBrainz soundtrack titles.

- Loads TMDb enrichment results and MB soundtrack metadata
- Applies consistent title cleaning (via reusable_cleaning)
- Uses rapidfuzz to compute fuzzy matches between titles (now using extractOne with row mapping)
- Logs confidence scores and exports best matches

Output:
- D:/Temp/mbdump/tmdb_fuzzy_matches.tsv

Used in:
- Step 4 EDA and feature engineering
"""

import pandas as pd
from rapidfuzz import process, fuzz
from reusable_cleaning import clean_title

# === FILE PATHS ===
MB_FILE = "D:/Temp/mbdump/soundtracks.parquet"
TMDB_FILE = "D:/Temp/mbdump/afi_enriched_tmdb.csv"
OUT_FILE = "D:/Temp/mbdump/tmdb_fuzzy_matches.tsv"

# === LOAD ===
print("📂 Loading MusicBrainz soundtracks...")
mb = pd.read_parquet(MB_FILE)
mb = mb.dropna(subset=["name_x"])

print("📂 Loading TMDb-enriched AFI titles...")
tmdb = pd.read_csv(TMDB_FILE)
tmdb = tmdb.dropna(subset=["input_title"])

# === NORMALIZE TITLES ===
mb["title_clean"] = mb["name_x"].apply(clean_title)
tmdb["title_clean"] = tmdb["input_title"].apply(clean_title)

# === FUZZY MATCH ===
print("🔎 Running fuzzy match with extractOne and row mapping...")
results = []
choices = {title: idx for idx, title in mb["title_clean"].items()}

for i, row in tmdb.iterrows():
    query = row["title_clean"]
    match_title, score, _ = process.extractOne(query, choices.keys(), scorer=fuzz.token_sort_ratio)
    mb_row = mb.loc[choices[match_title]]
    results.append({
        "tmdb_title": row["input_title"],
        "tmdb_genres": row["genres"],
        "tmdb_popularity": row["popularity"],
        "match_title": mb_row["name_x"],
        "match_artist": mb_row.get("name_y", ""),
        "fuzzy_score": score
    })
    print(f"✅ {row['input_title']}: best score = {score}")

# === EXPORT ===
df_out = pd.DataFrame(results)
df_out = df_out[df_out["fuzzy_score"] >= 80]  # optional filter

df_out.to_csv(OUT_FILE, sep="\t", index=False)
print(f"\n✅ Done. Matches saved to: {OUT_FILE}")
