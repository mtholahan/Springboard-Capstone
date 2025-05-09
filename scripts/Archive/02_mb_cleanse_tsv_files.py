"""
02_mb_cleanse_tsv_files.py

Reads MusicBrainz TSV files, ensures consistent UTF-8 encoding,
and writes out clean versions into a cleansed subfolder.
Adds known headers where appropriate.
"""

import os
from pathlib import Path
from config import MB_RAW_FILES, MB_TSV_FILES

# === Config ===
RAW_DIR = Path("D:/Capstone_Staging/data/musicbrainz_raw")
CLEAN_DIR = RAW_DIR / "cleansed"
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

# === Known headers for MB files ===
KNOWN_HEADERS = {
    "artist": [
        "id", "gid", "name", "sort_name", "begin_date_year", "begin_date_month",
        "begin_date_day", "end_date_year", "end_date_month", "end_date_day",
        "type", "area", "gender", "comment", "edits_pending", "last_updated",
        "ended", "begin_area", "end_area"
    ],
    "artist_credit": [
        "id", "name", "artist_count", "ref_count", "created", "edits_pending", "gid"
    ],
    "artist_credit_name": [
        "artist_credit", "position", "artist", "name", "join_phrase"
    ],
    "release": [
        "id", "gid", "name", "artist_credit", "release_group", "status", "packaging",
        "language", "script", "barcode", "comment", "edits_pending", "quality",
        "last_updated"
    ],
    "release_group": [
        "id", "gid", "name", "artist_credit", "type", "comment", "edits_pending", "last_updated"
    ],
    "release_group_secondary_type": [
        "id", "name", "parent", "child_order", "description", "gid"
    ],
    "release_group_secondary_type_join": [
        "release_group", "secondary_type", "created"
    ]
}

# === Main ===
def cleanse_file(src_path: Path, dest_path: Path, header: list[str] = None):
    line_count = 0
    with open(src_path, "r", encoding="utf-8", errors="replace") as src_file, \
         open(dest_path, "w", encoding="utf-8", newline="\n") as dest_file:
        
        if header:
            dest_file.write("\t".join(header) + "\n")

        for line in src_file:
            dest_file.write(line)
            line_count += 1

    return line_count

if __name__ == "__main__":
    print("🧼 Starting TSV cleansing...")

    for name, src_file in MB_RAW_FILES.items():
        dest_file = CLEAN_DIR / src_file.name
        header = KNOWN_HEADERS.get(name)
        print(f"→ Cleansing: {src_file.name}")
        lines = cleanse_file(src_file, dest_file, header=header)
        print(f"   Saved: {dest_file.name} ({lines:,} lines)")

    print(f"✅ All files cleansed and saved to: {CLEAN_DIR}")
