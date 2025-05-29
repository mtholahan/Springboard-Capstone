import pandas as pd
from rapidfuzz import process, fuzz
from pathlib import Path
from base_step import BaseStep
from config import DATA_DIR
import re
from utils import normalize_title, is_mostly_digits

class Step07MatchTMDb(BaseStep):
    def __init__(self, name="Step 07: Match TMDb Titles", threshold=90):
        super().__init__(name)
        self.input_movies = DATA_DIR / "tmdb" / "enriched_top_1000.csv"
        self.input_candidates = DATA_DIR / "tmdb" / "tmdb_input_candidates.csv"
        self.output_path = DATA_DIR / "tmdb" / "tmdb_match_results.csv"
        self.threshold = threshold

    def run(self):
        self.logger.info("🎬 Loading TMDb movie titles...")
        movies_df = pd.read_csv(self.input_movies)
        movies_df["normalized_title"] = movies_df["title"].apply(normalize_title)

        self.logger.info("🎧 Loading soundtrack candidates...")
        candidates_df = pd.read_csv(self.input_candidates)
        candidates_df["normalized_title"] = candidates_df["normalized_title"].astype(str)
        title_pool = candidates_df["normalized_title"].tolist()

        self.logger.info("🔍 Matching titles...")
        results = []
        misses = []
        for _, row in self.progress_iter(movies_df.iterrows(), total=len(movies_df), desc="TMDb Matching"):
            tmdb_title = row["normalized_title"]
            orig_title = row["title"]
            tmdb_id = row["tmdb_id"]
            year = row.get("release_year", "")

            match_result = process.extractOne(
                tmdb_title,
                title_pool,
                scorer=fuzz.ratio
            )

            if match_result is None:
                misses.append((orig_title, "<none>", 0))
                continue

            match, score, _ = match_result
            if score >= self.threshold:
                match_row = candidates_df[candidates_df["normalized_title"] == match].iloc[0]
                results.append({
                    "tmdb_id": tmdb_id,
                    "tmdb_title": orig_title,
                    "matched_title": match,
                    "release_year": year,
                    "score": score,
                    "release_group_id": match_row["release_group_id"]
                })
            else:
                misses.append((orig_title, match, score))

        output_df = pd.DataFrame(results)
        output_df.to_csv(self.output_path, index=False)
        self.logger.info(f"✅ Saved {len(output_df)} matches to {self.output_path}")

        # Log top misses for debugging
        if misses:
            self.logger.info("📉 Top 10 non-matching titles (below threshold):")
            for i, (tmdb_title, best_match, score) in enumerate(sorted(misses, key=lambda x: -x[2])[:10]):
                self.logger.info(f"{i+1}. {tmdb_title} → {best_match} ({score})")
