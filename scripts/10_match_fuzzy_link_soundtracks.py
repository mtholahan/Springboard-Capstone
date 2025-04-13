"""
10_match_fuzzy_link_soundtracks.py

Stable version with:
- Mojibake fix
- Alt-title substring & fuzzy fallback
- Optional year-based filtering
- Junk title blacklist
- Safe looping using .itertuples()
- Uses "clean" instead of "_clean" to avoid tuple attribute errors

Outputs:
- D:/Temp/mbdump/tmdb_fuzzy_matches.tsv
- D:/Temp/mbdump/tmdb_fuzzy_unmatched.tsv
"""

import pandas as pd
import requests
from pathlib import Path
from rapidfuzz import process, fuzz
from util_clean_title import clean_title

# === CONFIG ===
AFI_PATH = "D:/Temp/mbdump/tmdb_top_1000_enriched.csv"
MB_PATH = "D:/Temp/mbdump/soundtracks.parquet"
MANUAL_MATCH_PATH = "D:/Temp/mbdump/manual_matches.csv"
OUTPUT_MATCHED = "D:/Temp/mbdump/tmdb_fuzzy_matches.tsv"
OUTPUT_UNMATCHED = "D:/Temp/mbdump/tmdb_fuzzy_unmatched.tsv"
JUNK_LIST_PATH = "D:/Temp/mbdump/junk_mb_titles.txt"
TMDB_API_KEY = "8289cf63ae0018475953afaf51ce5464"

def fix_encoding(text):
    if isinstance(text, str):
        try:
            return text.encode('latin1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            return text
    return text

def fetch_alt_titles(tmdb_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/alternative_titles"
        r = requests.get(url, params={"api_key": TMDB_API_KEY})
        if r.status_code == 200:
            return [clean_title(t["title"]) for t in r.json().get("titles", []) if t.get("title")]
    except Exception:
        pass
    return []

print("📂 Loading MusicBrainz soundtracks...")
mb = pd.read_parquet(MB_PATH)

# Remove overrepresented titles
title_counts = mb["name_x"].value_counts()
mb = mb[~mb["name_x"].isin(title_counts[title_counts > 50].index)]

# Apply junk blacklist
if Path(JUNK_LIST_PATH).exists():
    with open(JUNK_LIST_PATH, "r", encoding="utf-8") as f:
        user_junk_titles = [line.strip().lower() for line in f if line.strip()]
    mb = mb[~mb["name_x"].str.lower().isin(user_junk_titles)]

# Generic and ASCII filtering
bad_titles = [
    "a soundtrack", "the soundtrack", "te soundtrack", "original score",
    "original soundtracks", "soundtrack to...", "oss soundtrack", "soundtrack v"
]
mb = mb[~mb["name_x"].str.lower().isin(bad_titles)]
mb = mb[mb["name_x"].str.len() > 10]
mb = mb[mb["name_x"].apply(lambda x: isinstance(x, str) and x.isascii())]

mb["clean"] = mb["name_x"].map(clean_title)

# Handle optional year column
mb_cols = ["clean", "name_x"]
if "year" in mb.columns:
    mb_cols.append("year")
mb_titles_all = mb.dropna(subset=["clean"])[mb_cols].drop_duplicates()

print("📂 Loading enriched TMDb titles...")
afi = pd.read_csv(AFI_PATH)
afi["input_title"] = afi["input_title"].map(fix_encoding)
afi["clean"] = afi["input_title"].map(clean_title)

print("📂 Loading manual matches...")
manual = pd.read_csv(MANUAL_MATCH_PATH) if Path(MANUAL_MATCH_PATH).exists() else pd.DataFrame(columns=["input_title", "manual_match_title"])
manual_dict = dict(zip(manual["input_title"], manual["manual_match_title"]))

results = []
unmatched = []

for _, row in afi.iterrows():
    raw_title = row["input_title"]
    norm_title = row["clean"]
    tmdb_id = row.get("tmdb_id")
    tmdb_year = row.get("tmdb_year", None)
    manual_match = manual_dict.get(raw_title)

    matched_title = None
    match_type = None
    score = 0

    if pd.notna(tmdb_year) and "year" in mb_titles_all.columns:
        mb_titles = mb_titles_all[mb_titles_all["year"].between(tmdb_year - 1, tmdb_year + 1)]
    else:
        mb_titles = mb_titles_all

    if manual_match:
        matched_title = manual_match
        match_type = "manual"
        score = 100
    else:
        for row_mb in mb_titles.itertuples(index=False):
            mb_clean = getattr(row_mb, "clean")
            mb_original = getattr(row_mb, "name_x")
            if not mb_clean or not mb_original:
                continue
            if norm_title in mb_clean or mb_clean in norm_title:
                matched_title = mb_original
                match_type = "substring"
                score = 100
                break

        if not matched_title and pd.notna(tmdb_id):
            alt_titles = fetch_alt_titles(tmdb_id)
            for alt in alt_titles:
                for row_mb in mb_titles.itertuples(index=False):
                    mb_clean = getattr(row_mb, "clean")
                    mb_original = getattr(row_mb, "name_x")
                    if not mb_clean or not mb_original:
                        continue
                    if alt in mb_clean or mb_clean in alt:
                        matched_title = mb_original
                        match_type = "alt_substring"
                        score = 100
                        break
                if matched_title:
                    break

        if not matched_title and pd.notna(tmdb_id):
            alt_titles = fetch_alt_titles(tmdb_id)
            for alt in alt_titles:
                best_match, score, _ = process.extractOne(
                    alt,
                    mb_titles["clean"],
                    scorer=fuzz.token_set_ratio
                )
                if score >= 90:
                    candidate = mb_titles[mb_titles["clean"] == best_match]["name_x"].values[0]
                    if (
                        candidate.lower().strip() not in bad_titles
                        and len(candidate.strip()) > 10
                        and candidate.isascii()
                    ):
                        matched_title = candidate
                        match_type = "alt_fuzzy"
                        break

        if not matched_title:
            mb_clean_list = mb_titles["clean"].tolist()
            best_match, score, _ = process.extractOne(
                norm_title,
                mb_clean_list,
                scorer=fuzz.token_set_ratio
            )
            if score >= 90:
                candidate = mb_titles[mb_titles["clean"] == best_match]["name_x"].values[0]
                if (
                    candidate.lower().strip() not in bad_titles
                    and len(candidate.strip()) > 10
                    and candidate.isascii()
                ):
                    matched_title = candidate
                    match_type = "fuzzy"

    if matched_title:
        results.append({
            "input_title": raw_title,
            "match_type": match_type,
            "best_mb_match": matched_title,
            "score": score
        })
        print(f"✅ {raw_title}: {match_type} match (score {score})")
    else:
        unmatched.append({
            "input_title": raw_title,
            "score": score,
            "notes": "No match above threshold"
        })
        print(f"❌ {raw_title}: No match")

pd.DataFrame(results).to_csv(OUTPUT_MATCHED, sep="\t", index=False)
pd.DataFrame(unmatched).to_csv(OUTPUT_UNMATCHED, sep="\t", index=False)
print(f"✅ Matches written to {OUTPUT_MATCHED}")
print(f"✅ Unmatched titles written to {OUTPUT_UNMATCHED}")
