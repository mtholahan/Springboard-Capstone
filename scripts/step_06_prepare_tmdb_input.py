# step_06_prepare_tmdb_input.py

import pandas as pd
import re
from pathlib import Path
from base_step import BaseStep
from config import DATA_DIR, MB_RAW_DIR
from utils import normalize_title, is_mostly_digits

class Step06PrepareTMDbInput(BaseStep):
    def __init__(self, name="Step 06: Prepare TMDb Input"):
        super().__init__(name)
        self.input_path = DATA_DIR / "soundtracks.tsv"
        self.junk_titles_path = MB_RAW_DIR / "junk_mb_titles.txt"
        self.output_path = DATA_DIR / "tmdb" / "tmdb_input_candidates.csv"

        # Define expected columns
        self.columns = [
            "release_group_id", "mbid", "title", "release_year", "artist_id", "artist_credit_id",
            "artist_name", "type", "primary_type", "barcode", "dummy_1",
            "dummy_2", "dummy_3", "dummy_4", "dummy_5", "artist_sort_name",
            "dummy_6", "dummy_7", "created", "dummy_8", "artist_gid"
        ]

    def run(self):
        if not self.input_path.exists():
            self.logger.error(f"Missing input file: {self.input_path}")
            return

        self.logger.info("🔍 Loading soundtracks...")
        df = pd.read_csv(self.input_path, sep="\t", names=self.columns, header=None, dtype=str)

        self.logger.info("🔧 Normalizing titles...")
        df["normalized_title"] = df["title"].apply(normalize_title)
        df = df[df["normalized_title"].str.len() >= 3]

        # Filter out bad or missing release years
        df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
        df = df[df["release_year"].between(1900, 2025)]
        df = df.dropna(subset=["release_year"])

        if self.junk_titles_path.exists():
            junk = set(self.junk_titles_path.read_text(encoding="utf-8").splitlines())
            df = df[~df["normalized_title"].isin(junk)]
            self.logger.info(f"🧼 Filtered junk titles — remaining: {len(df):,}")

        df = df.drop_duplicates(subset=["normalized_title"])
        output_df = df[["normalized_title", "release_group_id"]].copy()

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        output_df.to_csv(self.output_path, index=False)
        self.logger.info(f"✅ Final output row count: {len(output_df):,}")
        self.logger.info(f"✅ Saved to {self.output_path}")
