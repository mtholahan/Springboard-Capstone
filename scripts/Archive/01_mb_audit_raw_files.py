"""
01_mb_audit_raw_files.py

Audits the structure and contents of all MusicBrainz TSV files.
Includes file size, row counts, and character encoding tests.
Paths updated for Capstone staging area.
"""

import os
import datetime
from pathlib import Path
from config import MB_FILES

# === Config ===
RAW_DIR = Path("D:/Capstone_Staging/data/musicbrainz_raw")
OUTPUT_LOG = RAW_DIR / "mbdump_audit.txt"

# === Main ===
def audit_tsv_files():
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_logs = [f"=== MusicBrainz TSV Audit Report ({start_time}) ===\n"]

    for file_path in RAW_DIR.glob("*"):
        if file_path.is_file():
            name = file_path.name
            size_mb = round(file_path.stat().st_size / (1024 * 1024), 2)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    row_count = sum(1 for _ in f)
                encoding_status = "utf-8"
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    row_count = sum(1 for _ in f)
                encoding_status = "fallback"

            all_logs.append(f"{name}: {size_mb} MB, {row_count:,} lines [encoding: {encoding_status}]")

    with open(OUTPUT_LOG, "w", encoding="utf-8") as log_file:
        log_file.write("\n".join(all_logs))

    print(f"✅ Audit complete. Log saved to: {OUTPUT_LOG}")

if __name__ == "__main__":
    audit_tsv_files()
