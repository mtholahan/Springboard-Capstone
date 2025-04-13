"""
02_mb_cleanse_tsv_files.py

Cleans raw MusicBrainz TSV files for safe ingestion.

- Applies uniform UTF-8 encoding
- Replaces NULL values with "\\N"
- Strips blank strings and malformed lines
- Retains original column structure without headers

Processes these files:
- artist
- artist_credit
- artist_credit_name
- release
- release_group
- release_group_secondary_type_join
- release_group_secondary_type

Output:
- Cleaned versions of each file as `<name>_final.tsv` in the same directory
"""

import pandas as pd
from pathlib import Path

# List of TSV files to clean
files = [
    "artist",
    "artist_credit",
    "artist_credit_name",
    "release",
    "release_group",
    "release_group_secondary_type_join",
    "release_group_secondary_type"
]

input_dir = Path("D:/Temp/mbdump")
output_dir = input_dir  # or use a different path if you prefer

for name in files:
    input_path = input_dir / name
    output_path = output_dir / f"{name}_final.tsv"

    try:
        print(f"🧹 Cleaning {name}...")
        df = pd.read_csv(
            input_path,
            sep="\t",
            header=None,
            dtype=str,
            na_values=["\\N", ""],
            quoting=3,
            engine="python",
            on_bad_lines='warn'
        )
        df = df.fillna("\\N")
        df.to_csv(output_path, sep="\t", index=False, header=False, encoding="utf-8")
        print(f"✅ Saved cleaned file: {output_path.name}")
    except Exception as e:
        print(f"❌ Failed to clean {name}: {e}")
