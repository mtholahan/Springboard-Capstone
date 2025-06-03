# step_07_prepare_tmdb_input.py

from base_step import BaseStep
import pandas as pd
from config import DATA_DIR, MB_RAW_DIR, TMDB_DIR
from utils import normalize_title_for_matching, is_mostly_digits

class Step07PrepareTMDbInput(BaseStep):
    def __init__(self, name="Step 06: Prepare TMDb Input"):
        super().__init__(name)
        self.input_path = DATA_DIR / "soundtracks.tsv"
        self.junk_titles_path = MB_RAW_DIR / "junk_mb_titles.txt"
        self.output_path = TMDB_DIR / "tmdb_input_candidates.csv"

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
        df = pd.read_csv(self.input_path, sep='\t', names=self.columns, header=None, dtype=str)
        self.logger.info(f"Initial row count: {len(df):,}")

        self.logger.info("🔧 Normalizing titles...")
        df["normalized_title"] = df["title"].apply(normalize_title_for_matching)
        df = df[df["normalized_title"].str.len() >= 3]

        if self.junk_titles_path.exists():
            junk = set(self.junk_titles_path.read_text(encoding="utf-8").splitlines())
            before_junk = len(df)
            df = df[~df["normalized_title"].isin(junk)]
            after_junk = len(df)
            self.logger.info(f"🧼 Removed junk titles ({before_junk - after_junk:,}) — remaining: {after_junk:,}")

        before_numeric_filter = len(df)
        df = df[~df["normalized_title"].apply(is_mostly_digits)]
        after_numeric_filter = len(df)
        self.logger.info(f"🧹 Removed {before_numeric_filter - after_numeric_filter:,} mostly-numeric titles")

        self.logger.info("📆 Filtering by release_year...")
        df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
        df = df[df["release_year"].between(1900, 2025)]
        df = df.dropna(subset=["release_year"])

        self.logger.info("🧼 Dropping duplicates...")
        df = df.drop_duplicates(subset=["normalized_title"])

        df_out = df[["normalized_title", "release_group_id"]].copy()
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        df_out.to_csv(self.output_path, index=False)

        self.logger.info(f"✅ Final output row count: {len(df_out):,}")
        self.logger.info(f"✅ Saved to {self.output_path}")
