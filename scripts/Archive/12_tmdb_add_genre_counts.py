"""
12_tmdb_add_genre_counts.py

Reads the TMDb genre dimension and movie-genre link table.
Appends a 'Count' column to tmdb_genre_top_{TOP_N}.csv showing how many movies fall under each genre.
"""

import pandas as pd
from config import TMDB_GENRE_FILE, TMDB_MOVIE_GENRE_FILE

# --- Load genre dimension and link table ---
genres_df = pd.read_csv(TMDB_GENRE_FILE)
links_df = pd.read_csv(TMDB_MOVIE_GENRE_FILE)

# --- Print actual columns for debugging ---
print("🧪 Columns in movie-genre link table:", links_df.columns.tolist())

# --- Count how many times each genre appears ---
genre_counts = links_df["genre"].value_counts().reset_index()
genre_counts.columns = ["genre", "Count"]

# --- Merge back into genre dimension table ---
merged_df = genres_df.merge(genre_counts, on="genre", how="left")
merged_df["Count"] = merged_df["Count"].fillna(0).astype(int)

# --- Save updated genre file ---
merged_df.to_csv(TMDB_GENRE_FILE, index=False)
print(f"✅ Updated genre file saved with 'Count' column: {TMDB_GENRE_FILE}")
