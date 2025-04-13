"""
03_util_inspect_fieldnames.py

Utility script to inspect the structure of raw MusicBrainz `.tsv` files.

- Reads the first few rows of each file
- Reports number of columns and sample data
- Helps with column inference when headers are missing
- Outputs a JSON summary for documentation or schema review

Targeted files:
- artist_credit
- artist_credit_name
- release
- release_group
- release_group_secondary_type_join
- release_group_secondary_type

Output:
- D:/Temp/mbdump/tsv_inspection_summary.json
"""

import pandas as pd
from pathlib import Path

# Files we want to inspect
files = [
    "artist_credit",
    "artist_credit_name",
    "release",
    "release_group",
    "release_group_secondary_type_join",
    "release_group_secondary_type"
]

input_dir = Path("D:/Temp/mbdump")
results = {}

for name in files:
    input_path = input_dir / name
    try:
        print(f"🔍 Inspecting {name}...")
        df = pd.read_csv(input_path, sep="\t", header=None, nrows=5, dtype=str)
        results[name] = {
            "columns": df.shape[1],
            "sample": df.to_dict(orient="records")
        }
    except Exception as e:
        results[name] = {"error": str(e)}

# Save summary output
pd.Series(results).to_json("D:/Temp/mbdump/tsv_inspection_summary.json", indent=2)
print("✅ Summary saved to tsv_inspection_summary.json")
