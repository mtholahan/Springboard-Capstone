"""
rescue_map_builder.py

This script loads tmdb_fetch_errors.txt and extracts titles with zero matches.
It outputs:
- rescue_map_candidates.csv: for manual lookup and ID entry
- Optionally: rescue_map.json from the edited CSV

Usage:
  python rescue_map_builder.py --mode export
  python rescue_map_builder.py --mode generate
"""

import argparse
import pandas as pd
import json
from pathlib import Path

ERRORS_FILE = "tmdb_fetch_errors.txt"
CANDIDATE_CSV = "rescue_map_candidates.csv"
RESCUE_MAP_JSON = "rescue_map.json"

parser = argparse.ArgumentParser(description="Build a Rescue Map from zero-hit errors")
parser.add_argument("--mode", choices=["export", "generate"], required=True, help="export or generate the rescue map")
args = parser.parse_args()

if args.mode == "export":
    titles = []
    with open(ERRORS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "No good match above threshold" in line:
                title = line.split("|")[0].strip()
                titles.append(title)

    df = pd.DataFrame(sorted(set(titles)), columns=["mb_title"])
    df["tmdb_id"] = ""  # leave blank for manual entry
    df.to_csv(CANDIDATE_CSV, index=False)
    print(f"Exported {len(df)} unique titles to {CANDIDATE_CSV}")

elif args.mode == "generate":
    if not Path(CANDIDATE_CSV).exists():
        print("rescue_map_candidates.csv not found. Run export mode first.")
    else:
        df = pd.read_csv(CANDIDATE_CSV)
        df = df.dropna(subset=["tmdb_id"])
        df = df[df.tmdb_id.astype(str).str.strip() != ""]
        rescue_map = {
            row["mb_title"].lower().strip(): int(row["tmdb_id"])
            for _, row in df.iterrows()
        }
        with open(RESCUE_MAP_JSON, "w", encoding="utf-8") as f:
            json.dump(rescue_map, f, indent=2)
        print(f"Wrote {len(rescue_map)} entries to {RESCUE_MAP_JSON}")
