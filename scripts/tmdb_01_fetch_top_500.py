"""
tmdb_01_fetch_top_500.py

Fetches the top 500 rated movies from TMDb and saves to D:/Capstone_Staging/data/tmdb/tmdb_top_500.csv
"""

import requests
import pandas as pd
from time import sleep
from pathlib import Path

API_KEY = "8289cf63ae0018475953afaf51ce5464"
BASE_URL = "https://api.themoviedb.org/3/movie/top_rated"

movies = []

for page in range(1, 26):  # 25 pages × 20 = 500
    print(f"Fetching page {page}...")
    response = requests.get(BASE_URL, params={"api_key": API_KEY, "page": page})
    response.raise_for_status()
    data = response.json()
    for m in data["results"]:
        movies.append({
            "tmdb_id": m["id"],
            "title": m["title"],
            "release_year": m["release_date"][:4] if m.get("release_date") else None
        })
    sleep(0.2)

# --- Save to target path ---
output_path = Path("D:/Capstone_Staging/data/tmdb/tmdb_top_500.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(movies)
df.to_csv(output_path, index=False)
print(f"✅ Done! Saved to {output_path}")
