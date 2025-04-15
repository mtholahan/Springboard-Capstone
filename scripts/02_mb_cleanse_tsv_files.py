"""
02_mb_cleanse_tsv_files.py

Reads MusicBrainz TSV files, ensures consistent UTF-8 encoding,
and writes out clean versions into a cleansed subfolder.
Only cleanses whitelisted files.
"""

import os
from pathlib import Path
from config import MB_FILES

# === Config ===
RAW_DIR = Path("D:/Capstone_Staging/data/musicbrainz_raw")
CLEAN_DIR = RAW_DIR / "cleansed"
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

# === Main ===
def cleanse_file(src_path: Path, dest_path: Path):
    line_count = 0
    with open(src_path, "r", encoding="utf-8", errors="replace") as src_file, \
         open(dest_path, "w", encoding="utf-8", newline="\n") as dest_file:
        for line in src_file:
            dest_file.write(line)
            line_count += 1
    return line_count

if __name__ == "__main__":
    print("🧼 Starting TSV cleansing...")
    for name, src_file in MB_FILES.items():
        dest_file = CLEAN_DIR / src_file.name
        print(f"→ Cleansing: {src_file.name}")
        lines = cleanse_file(src_file, dest_file)
        print(f"   Saved: {dest_file.name} ({lines:,} lines)")

    print(f"✅ All files cleansed and saved to: {CLEAN_DIR}")
