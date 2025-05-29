import pandas as pd
import re
from pathlib import Path

input_path = Path("D:/Capstone_Staging/data/soundtracks.tsv")
junk_titles_path = Path("D:/Capstone_Staging/data/musicbrainz_raw/junk_mb_titles.txt")
output_path = Path("D:/Capstone_Staging/data/tmdb/tmdb_input_candidates.csv")

columns = [
    "release_group_id", "mbid", "title", "release_year", "artist_id", "artist_credit_id",
    "artist_name", "type", "primary_type", "barcode", "dummy_1",
    "dummy_2", "dummy_3", "dummy_4", "dummy_5", "artist_sort_name",
    "dummy_6", "dummy_7", "created", "dummy_8", "artist_gid"
]

def normalize_title(title):
    if pd.isna(title):
        return ""
    return re.sub(r"[^a-z0-9\s]", "", title.lower()).strip()

print("🔍 Loading data...")
df = pd.read_csv(input_path, sep='\t', names=columns, header=None, dtype=str)
print(f"Initial row count: {len(df):,}")

print("🔧 Normalizing titles...")
df["normalized_title"] = df["title"].apply(normalize_title)
df = df[df["normalized_title"].str.len() >= 3]

if junk_titles_path.exists():
    junk = set(junk_titles_path.read_text(encoding="utf-8").splitlines())
    df = df[~df["normalized_title"].isin(junk)]

print("📆 Filtering by release_year...")
df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
df = df[df["release_year"].between(1900, 2025)]
df = df.dropna(subset=["release_year"])

print("🧼 Dropping duplicates...")
df = df.drop_duplicates(subset=["normalized_title"])

df_out = df[["normalized_title", "release_group_id"]].copy()
output_path.parent.mkdir(parents=True, exist_ok=True)
df_out.to_csv(output_path, index=False

print(f"✅ Final output row count: {len(df_out):,}")
print(f"✅ Saved to {output_path}")
