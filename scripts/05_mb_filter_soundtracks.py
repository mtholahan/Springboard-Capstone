"""
05_mb_filter_soundtracks.py

Filters release_group_joined.tsv for entries that are likely to be
soundtracks or scores. Saves the filtered results as a separate TSV.
"""

import pandas as pd
from pathlib import Path
from config import MB_FILES

# === Config ===
RAW_DIR = Path("D:/Capstone_Staging/data/musicbrainz_raw")
JOINED_FILE = RAW_DIR / "release_group_joined.tsv"
OUTPUT_FILE = RAW_DIR / "release_group_soundtracks.tsv"

# === Load Joined Data ===
print("🎼 Loading full release_group_joined.tsv...")
df = pd.read_csv(JOINED_FILE, sep="\t", dtype=str, encoding="utf-8", on_bad_lines="skip")
print("🔍 Full dataset shape:", df.shape)
print("🧪 Columns in release_group_joined:", df.columns.tolist())

# === Filter Logic ===
pattern = r"soundtrack|original motion picture|score|ost"
filtered = df[df["name_x"].str.contains(pattern, case=False, na=False)]
print(f"🎯 Matched entries: {len(filtered):,} rows")

# Preview matches
print("🔎 Sample titles:")
print(filtered[["name_x"]].dropna().sample(n=min(10, len(filtered)), random_state=42))

# === Output ===
filtered.to_csv(OUTPUT_FILE, sep="\t", index=False, encoding="utf-8")
print(f"✅ Filtered soundtracks written to: {OUTPUT_FILE}")
