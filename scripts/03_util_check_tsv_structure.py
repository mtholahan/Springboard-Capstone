"""
03_util_check_tsv_structure.py

Inspects the first line (headers) of each MusicBrainz TSV file
in the configured staging folder. Reports column counts and saves
a JSON summary of the results with basic field diagnostics.
"""

import json
from pathlib import Path
from config import MB_FILES

# === Config ===
RAW_DIR = Path("D:/Capstone_Staging/data/musicbrainz_raw")
SUMMARY_FILE = RAW_DIR / "tsv_inspection_summary.json"

# === Main ===
def inspect_headers():
    summary = {}
    for name, tsv_file in MB_FILES.items():
        try:
            with open(tsv_file, "r", encoding="utf-8", errors="replace") as f:
                header_line = f.readline().strip()
                header_fields = header_line.split("\t")
                summary[name] = {
                    "num_fields": len(header_fields),
                    "fields": header_fields
                }
        except Exception as e:
            summary[name] = {"error": str(e)}

    with open(SUMMARY_FILE, "w", encoding="utf-8") as out:
        json.dump(summary, out, indent=2)

    print(f"✅ Header inspection complete. Summary saved to: {SUMMARY_FILE}")

if __name__ == "__main__":
    inspect_headers()
