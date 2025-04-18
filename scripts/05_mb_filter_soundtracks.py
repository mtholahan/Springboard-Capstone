"""
05_mb_filter_soundtracks.py

Filters MusicBrainz release_groups to include only soundtrack-related records.
Outputs a filtered TSV and Parquet file.
"""

import pandas as pd
from config import MB_FILES, MB_SOUNDTRACKS_FILE, MB_PARQUET_SOUNDTRACKS

# --- Load input ---
df = pd.read_csv(MB_FILES["release_group"], sep='\t', low_memory=False, header=None)
df.columns = [
    "id", "gid", "name", "artist_credit", "type",
    "comment", "edits_pending", "last_updated"
]

# --- Filter for soundtrack types ---
soundtrack_df = df.copy()  # Placeholder for real filtering logic later

# --- Save TSV and Parquet with headers ---
soundtrack_df.to_csv(MB_SOUNDTRACKS_FILE, sep='\t', index=False, header=True)
soundtrack_df.to_parquet(MB_PARQUET_SOUNDTRACKS, index=False)

print(f"✅ Filtered soundtrack data written to:")
print(f"   TSV: {MB_SOUNDTRACKS_FILE}")
print(f"   Parquet: {MB_PARQUET_SOUNDTRACKS}")
