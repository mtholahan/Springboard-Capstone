import pandas as pd

# Load the TMDb enriched movie dataset
df = pd.read_csv("D:/Temp/mbdump/tmdb_top_1000_enriched.csv")

# Extract tmdb_id and genres, dropping any rows without genres
df_genres = df[["tmdb_id", "genres"]].dropna()

# Split genre strings and explode into individual rows
df_genres["genre"] = df_genres["genres"].str.split("|")
df_exploded = df_genres.explode("genre").drop(columns=["genres"]).dropna()

# Create genre lookup table with genre_id
df_genre_lookup = (
    df_exploded[["genre"]]
    .drop_duplicates()
    .reset_index(drop=True)
    .reset_index()
    .rename(columns={"index": "genre_id", "genre": "name"})
)

# Map genre names to IDs in movie-genre table
genre_map = dict(zip(df_genre_lookup["name"], df_genre_lookup["genre_id"]))
df_movie_genre = df_exploded.copy()
df_movie_genre["genre_id"] = df_movie_genre["genre"].map(genre_map)
df_movie_genre = df_movie_genre[["tmdb_id", "genre_id"]]

# Save to CSV
df_genre_lookup.to_csv("D:/Temp/mbdump/tmdb_genre.csv", index=False)
df_movie_genre.to_csv("D:/Temp/mbdump/tmdb_movie_genre.csv", index=False)

print("✅ Genre normalization complete. Files written to D:/Temp/mbdump/")
