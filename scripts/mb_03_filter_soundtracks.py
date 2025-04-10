"""
mb_03_filter_soundtracks.py

Filters joined MusicBrainz data to include only soundtrack-related entries.

- Loads the full joined release group dataset
- Filters where secondary_type_name == 'Soundtrack'
- Saves as both TSV (readable) and Parquet (performance)

Outputs:
- D:/Temp/mbdump/soundtracks.tsv
- D:/Temp/mbdump/soundtracks.parquet

Used by:
- match_05_fuzzy_afi_mb.py (for matching TMDb titles to MB soundtracks)
"""

import pandas as pd
from pathlib import Path

# === CONFIG ===
DATA_DIR = Path("D:/Temp/mbdump")
JOINED_FILE = DATA_DIR / "release_group_joined.tsv"
OUT_TSV = DATA_DIR / "soundtracks.tsv"
OUT_PARQUET = DATA_DIR / "soundtracks.parquet"

# === LOAD ===
df = pd.read_csv(JOINED_FILE, sep="\t", dtype=str)
print(f"📦 Loaded joined dataset: {df.shape}")

# === FILTER ===
soundtracks = df[df["secondary_type_name"] == "Soundtrack"]
print(f"🎵 Soundtrack rows found: {soundtracks.shape[0]}")

# === NULL CHECK ===
print("\n🕵️ Nulls per column (soundtracks only):")
print(soundtracks.isnull().sum())

# === EXPORT ===
soundtracks.to_csv(OUT_TSV, sep="\t", index=False)
print(f"✅ Exported to: {OUT_TSV}")

try:
    soundtracks.to_parquet(OUT_PARQUET, index=False)
    print(f"✅ Parquet version exported to: {OUT_PARQUET}")
except Exception as e:
    print(f"⚠️ Could not export Parquet: {e}")
