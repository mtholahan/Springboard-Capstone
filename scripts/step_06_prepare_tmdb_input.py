import pandas as pd
from pathlib import Path
import re

# --- Config ---
INPUT_SOUNDTRACKS = Path("D:/Capstone_Staging/data/soundtracks.tsv")
JUNK_TITLES_FILE = Path("D:/Capstone_Staging/data/musicbrainz_raw/junk_mb_titles.txt")
OUTPUT_CANDIDATES = Path("D:/Capstone_Staging/data/tmdb/tmdb_input_candidates.csv")

# --- Load soundtrack columns ---
soundtrack_cols = [
    "release_group_id", "mbid", "title", "release_year", "artist_id", "artist_credit_id",
    "artist_name", "type", "primary_type", "barcode", "dummy_1",
    "dummy_2", "dummy_3", "dummy_4", "dummy_5", "artist_sort_name",
    "dummy_6", "dummy_7", "created", "dummy_8", "artist_gid"
]

def normalize_title(title):
    if pd.isna(title):
        return ""
    return re.sub(r"[^a-z0-9\s]", "", title.lower()).strip()

def main():
    print("🔍 Loading soundtracks...")
    df = pd.read_csv(INPUT_SOUNDTRACKS, sep="\t", names=soundtrack_cols, header=None, dtype=str)

    print("🔧 Normalizing titles...")
    df["normalized_title"] = df["title"].apply(normalize_title)
    df = df[df["normalized_title"].str.len() >= 3]

    if JUNK_TITLES_FILE.exists():
        junk = set(Path(JUNK_TITLES_FILE).read_text(encoding="utf-8").splitlines())
        df = df[~df["normalized_title"].isin(junk)]

    print("🧼 Filtering duplicates and junk...")
    df = df.drop_duplicates(subset=["normalized_title"])
    output_df = df[["normalized_title", "release_group_id"]].copy()

    print(f"✅ Final output row count: {len(output_df):,}")
    OUTPUT_CANDIDATES.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(OUTPUT_CANDIDATES, index=False)
    print(f"✅ Saved to {OUTPUT_CANDIDATES}")

if __name__ == "__main__":
    main()
