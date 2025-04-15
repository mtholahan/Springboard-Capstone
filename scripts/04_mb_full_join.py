"""
04_mb_full_join.py

Joins core MusicBrainz tables: release_group, secondary_type, join mappings.
Preserves intermediate outputs and sanity checks. Config-based paths.
"""

import pandas as pd
from pathlib import Path
from config import MB_FILES

# === Config ===
RAW_DIR = Path("D:/Capstone_Staging/data/musicbrainz_raw")
OUTPUT_DIR = RAW_DIR

# === Load Source Files ===
print("📥 Loading source TSV files...")
release_group = pd.read_csv(
    MB_FILES["release_group"],
    sep="\t",
    header=None,
    names=["id", "gid", "name", "artist_credit", "type", "comment", "edits_pending", "last_updated"],
    dtype=str,
    encoding="utf-8",
    on_bad_lines="skip"
)

rg_secondary_type = pd.read_csv(
    MB_FILES["release_group_secondary_type"],
    sep="\t",
    header=None,
    names=["id", "gid", "name", "comment", "edits_pending", "last_updated"],
    dtype=str,
    encoding="utf-8",
    on_bad_lines="skip"
)

rg_secondary_type_join = pd.read_csv(
    MB_FILES["release_group_secondary_type_join"],
    sep="\t",
    header=None,
    names=["release_group", "secondary_type"],
    dtype=str,
    encoding="utf-8",
    on_bad_lines="skip"
)

print("🔍 release_group shape:", release_group.shape)
print("🔍 secondary_type shape:", rg_secondary_type.shape)
print("🔍 secondary_type_join shape:", rg_secondary_type_join.shape)
print("🧪 Columns in secondary_type_join:", rg_secondary_type_join.columns.tolist())
print("🧪 Columns in rg_secondary_type:", rg_secondary_type.columns.tolist())

# === Intermediate Outputs ===
release_group.to_csv(OUTPUT_DIR / "release_group_clean.tsv", sep="\t", index=False, encoding="utf-8")
rg_secondary_type.to_csv(OUTPUT_DIR / "release_group_secondary_type_clean.tsv", sep="\t", index=False, encoding="utf-8")
rg_secondary_type_join.to_csv(OUTPUT_DIR / "release_group_secondary_type_join_clean.tsv", sep="\t", index=False, encoding="utf-8")

# === Merge ===
print("🔗 Joining release_group → secondary_type_join...")
df = release_group.merge(rg_secondary_type_join, how="left", left_on="id", right_on="release_group")
print("→ After join #1:", df.shape)

print("🔗 Joining with secondary_type...")
df = df.merge(rg_secondary_type, how="left", left_on="secondary_type", right_on="id")
print("→ After join #2:", df.shape)

# === Final Output ===
output_path = OUTPUT_DIR / "release_group_joined.tsv"
df.to_csv(output_path, sep="\t", index=False, encoding="utf-8")
print(f"✅ Final joined file written to: {output_path} ({df.shape[0]:,} rows)")
