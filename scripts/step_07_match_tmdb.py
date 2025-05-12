import pandas as pd
from rapidfuzz import process, fuzz
from pathlib import Path
from tqdm import tqdm
import re

# --- Config ---
INPUT_MOVIES = Path("D:/Capstone_Staging/data/tmdb/enriched_top_1000.csv")
INPUT_CANDIDATES = Path("D:/Capstone_Staging/data/tmdb/tmdb_input_candidates.csv")
OUTPUT_MATCHES = Path("D:/Capstone_Staging/data/tmdb/tmdb_match_results.csv")
SIMILARITY_THRESHOLD = 90

# --- Helper ---
def normalize(text):
    if pd.isna(text):
        return ""
    return re.sub(r"[^a-z0-9\s]", "", text.lower()).strip()

def main():
    print("🎬 Loading movie titles...")
    movies_df = pd.read_csv(INPUT_MOVIES)
    movies_df["normalized_title"] = movies_df["title"].apply(normalize)

    print("🎧 Loading soundtrack candidates...")
    candidates_df = pd.read_csv(INPUT_CANDIDATES)
    candidates_df["normalized_title"] = candidates_df["normalized_title"].astype(str)
    title_pool = candidates_df["normalized_title"].tolist()

    print("🔍 Matching titles...")
    results = []
    for _, row in tqdm(movies_df.iterrows(), total=len(movies_df), desc="TMDb Matching"):
        tmdb_title = row["normalized_title"]
        orig_title = row["title"]
        tmdb_id = row["tmdb_id"]
        year = row.get("release_year", "")

        match, score, _ = process.extractOne(
            tmdb_title,
            title_pool,
            scorer=fuzz.ratio
        )

        if score >= SIMILARITY_THRESHOLD:
            match_row = candidates_df[candidates_df["normalized_title"] == match].iloc[0]
            results.append({
                "tmdb_id": tmdb_id,
                "tmdb_title": orig_title,
                "matched_title": match,
                "release_year": year,
                "score": score,
                "release_group_id": match_row["release_group_id"]
            })

    output_df = pd.DataFrame(results)
    output_df.to_csv(OUTPUT_MATCHES, index=False)
    print(f"✅ Done. Saved {len(output_df)} matches to {OUTPUT_MATCHES}")

if __name__ == "__main__":
    main()
