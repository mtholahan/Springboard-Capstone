"""
05_mb_filter_soundtracks.py

Filters the MusicBrainz release_group and release tables to keep only soundtrack-related entries.
Saves the result as a Parquet file for use in fuzzy matching (Script 11).
"""

import pandas as pd
from pathlib import Path
from config import MB_PARQUET_SOUNDTRACKS, MB_SECONDARY_TYPE_JOIN_FILE

# --- Define input file paths (no extensions) ---
MB_TSV_DIR = MB_PARQUET_SOUNDTRACKS.parent
RELEASE_FILE = MB_TSV_DIR / "release"
RELEASE_GROUP_FILE = MB_TSV_DIR / "release_group"
SECONDARY_TYPE_FILE = MB_TSV_DIR / "release_group_secondary_type"

# --- Load datasets with logging ---
print("📥 Loading release_group...")
rg = pd.read_csv(
    RELEASE_GROUP_FILE,
    sep="\t",
    header=None,
    names=["id", "gid", "name", "artist_credit", "type", "comment", "edits_pending", "last_updated"],
    dtype=str
)
print(f"✅ Loaded release_group ({len(rg):,} rows)")

print("📥 Loading release_group_secondary_type_join...")
rgs_join = pd.read_csv(
    MB_SECONDARY_TYPE_JOIN_FILE,
    sep="\t",
    header=None,
    names=["release_group", "secondary_type"],
    dtype=str
)
print(f"✅ Loaded release_group_secondary_type_join ({len(rgs_join):,} rows)")

print("📥 Loading release_group_secondary_type...")
rgs_type = pd.read_csv(
    SECONDARY_TYPE_FILE,
    sep="\t",
    header=None,
    names=["id", "name", "parent", "child_order", "description", "gid"],
    dtype=str
)
print(f"✅ Loaded release_group_secondary_type ({len(rgs_type):,} rows)")

print("📥 Loading release (this one takes a bit)...")
release = pd.read_csv(
    RELEASE_FILE,
    sep="\t",
    header=None,
    names=["id", "gid", "name", "artist_credit", "release_group", "status", "packaging", "language", "script", "barcode", "comment", "edits_pending", "quality", "last_updated"],
    dtype=str
)
print(f"✅ Loaded release ({len(release):,} rows)")

# --- Identify soundtrack type IDs ---
print("🔍 Available secondary types:")
print(rgs_type[["id", "name"]])

soundtrack_type_ids = rgs_type[rgs_type["name"].str.lower().str.contains("soundtrack|score", regex=True)]["id"].tolist()
print("🎼 Matched soundtrack/score type IDs:", soundtrack_type_ids)

# --- Find matching release group IDs ---
matched_rg_ids = rgs_join[rgs_join["secondary_type"].isin(soundtrack_type_ids)]["release_group"].unique()
print(f"🔗 Matched release_group IDs: {len(matched_rg_ids):,}")

# --- Filter releases by release_group ---
filtered_releases = release[release["release_group"].isin(matched_rg_ids)]

# --- Save filtered results ---
filtered_releases.to_parquet(MB_PARQUET_SOUNDTRACKS, index=False)
print(f"✅ Saved {len(filtered_releases):,} soundtrack releases to: {MB_PARQUET_SOUNDTRACKS}")
