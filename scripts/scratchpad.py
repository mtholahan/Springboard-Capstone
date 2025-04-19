import pandas as pd
from config import BASE_DIR

mb_dir = BASE_DIR / "data" / "musicbrainz_raw"

# Load cleaned join table (2 columns)
join = pd.read_csv(mb_dir / "release_group_secondary_type_join_clean.tsv", sep="\t", dtype=str)

# Load release table
release = pd.read_csv(
    mb_dir / "release",
    sep="\t",
    header=None,
    names=[
        "id", "gid", "name", "artist_credit", "release_group", "status", "packaging",
        "language", "script", "barcode", "comment", "edits_pending", "quality", "last_updated"
    ],
    dtype=str
)

# How many of the release_group IDs actually appear in the release table?
rg_ids = set(join[join["secondary_type"] == "2"]["release_group"])
release_rg_ids = set(release["release_group"])

matching = rg_ids & release_rg_ids

print(f"🎯 release_group IDs in join file: {len(rg_ids):,}")
print(f"📦 release_group IDs in release file: {len(release_rg_ids):,}")
print(f"✅ Matching IDs found: {len(matching):,}")
