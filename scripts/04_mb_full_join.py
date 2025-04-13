"""
04_mb_full_join.py

Joins key MusicBrainz datasets:
- release_group: MusicBrainz release metadata (ID, name, type, etc.)
- artist_credit_name: Maps release_group to artist name
- release_group_secondary_type: Captures labels like 'Soundtrack'

Performs:
- Tab-separated file loads with robust parsing (handles extra columns)
- Inner joins across IDs
- Output dataset with release title, artist, and secondary type
- Exports full TSV and filtered Parquet

Output:
- D:/Temp/mbdump/release_group_joined.tsv (full join)
- D:/Temp/mbdump/soundtracks.parquet (only soundtrack rows)

Used by:
- mb_03_filter_soundtracks.py
- match_05_fuzzy_afi_mb.py
"""

import pandas as pd
from pathlib import Path
import psutil
from datetime import datetime

# === CONFIG ===
DATA_DIR = Path("D:/Temp/mbdump")
OUTPUT_TSV = DATA_DIR / "release_group_joined.tsv"
OUTPUT_PARQUET = DATA_DIR / "soundtracks.parquet"

# === RAM MONITOR ===
def log_ram():
    used = psutil.Process().memory_info().rss / 1024**2
    print(f"[{datetime.now()}] 🧠 RAM used: {used:.2f} MB")

# === FILE LOADER (Robust) ===
def load_file(filename, n_cols_expected):
    file_path = DATA_DIR / filename
    print(f"📂 Loading {filename} — expecting ~{n_cols_expected} columns")
    df = pd.read_csv(
        file_path,
        sep="\t",
        header=None,
        dtype=str,
        na_values=["\\N"],
        engine="python",
        on_bad_lines="skip"
    )
    df.columns = [f"col{i}" for i in range(df.shape[1])]
    print(f"✅ Loaded {filename}: {df.shape}")
    log_ram()
    return df

# === LOAD FILES ===
release_group = load_file("release_group", 8)
release_group.columns = ["id", "gid", "name", "artist_credit", "type", "comment", "edits_pending", "last_updated"]

artist_credit_name = load_file("artist_credit_name", 5)
artist_credit_name.columns = ["artist_credit", "position", "artist", "name", "join_phrase"]

secondary_type = load_file("release_group_secondary_type", 2)
secondary_type = secondary_type.iloc[:, :2]  # only use first 2 columns
secondary_type.columns = ["release_group", "secondary_type"]

# === JOIN LOGIC ===
df = release_group.merge(artist_credit_name, on="artist_credit", how="inner")
df = df.merge(secondary_type, left_on="id", right_on="release_group", how="left")

print(f"🔗 After join: {df.shape}")

# === EXPORT FULL TSV ===
df.to_csv(OUTPUT_TSV, sep="\t", index=False)
print(f"✅ Exported full join to: {OUTPUT_TSV}")

# === EXPORT SOUNDTRACKS PARQUET ===
soundtracks = df[df["secondary_type"].str.lower() == "soundtrack"]
soundtracks.to_parquet(OUTPUT_PARQUET, index=False)
print(f"✅ Exported soundtrack subset to: {OUTPUT_PARQUET}")
