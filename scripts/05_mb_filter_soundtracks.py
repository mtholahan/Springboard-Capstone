"""
05_mb_filter_soundtracks.py

Filters the full MusicBrainz joined dataset to extract likely soundtrack-related entries.

- Loads release_group_joined.tsv from previous join step
- Applies broad filters on 'secondary_type' and name content
- Exports result to soundtracks.parquet for matching & analysis
- Includes sanity checks on record count

Output:
- D:/Temp/mbdump/soundtracks.parquet

Used in:
- match_05_fuzzy_afi_mb.py (fuzzy match to TMDb titles)
"""

import pandas as pd
from pathlib import Path
import sys

INPUT_FILE = "D:/Temp/mbdump/release_group_joined.tsv"
OUTPUT_FILE = "D:/Temp/mbdump/soundtracks.parquet"

# === LOAD FULL JOIN ===
df = pd.read_csv(INPUT_FILE, sep="\t", dtype=str)
print(f"📂 Loaded joined dataset: {df.shape[0]:,} rows")

# === FILTER SOUNDTRACK-LIKE ENTRIES ===
mask = (
    df["secondary_type"].str.contains("soundtrack|score", case=False, na=False) |
    df["name_x"].str.contains("soundtrack|original score|motion picture|ost", case=False, na=False)
)
soundtracks = df[mask].copy()
print(f"🎯 Soundtrack candidates: {soundtracks.shape[0]:,} rows")

# === EXPORT ===
soundtracks.to_parquet(OUTPUT_FILE, index=False)
print(f"✅ Saved: {OUTPUT_FILE}")

# === SANITY CHECK ===
verify = pd.read_parquet(OUTPUT_FILE)
count = verify.shape[0]
print(f"🔎 Parquet verification: {count:,} records loaded")

# === MINIMUM ROW COUNT CHECK ===
if count < 100:
    raise ValueError(f"🚨 Too few records in Parquet file: only {count} found. Aborting.")
