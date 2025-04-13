"""
01_mb_audit_raw_files.py

Audits all `.tsv` files in the MusicBrainz dump folder.

For each file:
- Loads 5–10 sample rows
- Logs column names, data types, null counts, and sample values
- Outputs a persistent audit report

Output:
- D:/Temp/mbdump/mbdump_audit.txt

Purpose:
Create a permanent reference to all raw TSV file structures.
"""

import os
import pandas as pd
from pathlib import Path
from datetime import datetime

# === CONFIG ===
DATA_DIR = Path("D:/Temp/mbdump")
OUTPUT_LOG = DATA_DIR / "mbdump_audit.txt"
N_ROWS = 10

def audit_tsv(file_path, n_rows=10):
    try:
        df = pd.read_csv(file_path, sep="\t", nrows=n_rows, dtype=str, na_values=["\\N"])
        log = []
        log.append(f"--- {file_path.name} ---")
        log.append(f"✅ Rows loaded: {len(df)}")
        log.append(f"✅ Columns: {df.shape[1]} -> {list(df.columns)}")
        log.append(f"✅ Data Types:\n{df.dtypes}")
        log.append(f"✅ Null Counts:\n{df.isnull().sum()}")
        log.append(f"✅ Sample Rows:\n{df.head().to_string(index=False)}")
        return "\n".join(log) + "\n"
    except Exception as e:
        return f"❌ Error loading {file_path.name}: {e}\n"

def main():
    start_time = datetime.now()
    print(f"[{start_time}] Starting TSV audit in: {DATA_DIR}")
    all_logs = [f"=== MusicBrainz TSV Audit Report ({start_time}) ===\n"]
    
    data_files = [f for f in sorted(DATA_DIR.iterdir()) if f.is_file()]
    print(f"📂 Found {len(data_files)} files in {DATA_DIR}")
    
    for file in data_files:
        log = audit_tsv(file, N_ROWS)
        all_logs.append(log)
        print(f"Audited: {file.name}")

    OUTPUT_LOG.write_text("\n".join(all_logs), encoding="utf-8")
    end_time = datetime.now()
    print(f"[{end_time}] Audit complete. Output saved to: {OUTPUT_LOG}")

if __name__ == "__main__":
    main()
