"""
09_tmdb_normalize_genres.py

Explode comma-separated genre strings from TMDb into a normalized format.
"""

import pandas as pd
from config import TMDB_FILES

INPUT_CSV = TMDB_FILES["enriched_top_1000"]
MOVIE_GENRE_OUT = TMDB_FILES["enriched_top_1000"].with_name("tmdb_movie_genre.csv")
GENRE_DIM_OUT = TMDB_FILES["enriched_top_1000"].with_name("tmdb_genre.csv")

# --- LOAD ---
df = pd.read_csv(INPUT_CSV)
df = df.dropna(subset=["genres"])

# --- NORMALIZE ---
all_genres = set()
movie_genre_records = []

for _, row in df.iterrows():
    genres = [g.strip() for g in row["genres"].split(",") if g.strip()]
    for genre in genres:
        all_genres.add(genre)
        movie_genre_records.append({
            "tmdb_id": row["tmdb_id"],
            "genre": genre
        })

genre_dim = pd.DataFrame(sorted(all_genres), columns=["genre"])
movie_genre = pd.DataFrame(movie_genre_records)

# --- SAVE ---
genre_dim.to_csv(GENRE_DIM_OUT, index=False)
movie_genre.to_csv(MOVIE_GENRE_OUT, index=False)

print(f"✅ Normalized genres written to:\n- {GENRE_DIM_OUT}\n- {MOVIE_GENRE_OUT}")
