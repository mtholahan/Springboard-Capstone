"""
09_tmdb_normalize_genres.py

Explode comma-separated genre strings from TMDb into normalized format.
Input: Enriched Top N file
Outputs: Normalized genre and movie-genre lookup tables
"""

import pandas as pd
from config import ENRICHED_FILE, TMDB_GENRE_FILE, TMDB_MOVIE_GENRE_FILE

# --- LOAD ---
df = pd.read_csv(ENRICHED_FILE)
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

# --- CONSTRUCT TABLES ---
genre_dim = pd.DataFrame(sorted(all_genres), columns=["genre"])
movie_genre = pd.DataFrame(movie_genre_records)

# --- SAVE ---
genre_dim.to_csv(TMDB_GENRE_FILE, index=False)
movie_genre.to_csv(TMDB_MOVIE_GENRE_FILE, index=False)

print(f"✅ Normalized genres written to:\n- {TMDB_GENRE_FILE}\n- {TMDB_MOVIE_GENRE_FILE}")
