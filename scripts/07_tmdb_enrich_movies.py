"""
07_tmdb_enrich_movies.py

Enriches a list of TMDb movies with additional metadata via API calls.

- Reads from a user-specified CSV (must contain TMDb IDs and titles)
- Calls TMDb's /movie/{id} endpoint for details
- Adds genre names, media type, fuzzy score placeholder
- Outputs enriched data to CSV

Usage:
python 07_tmdb_enrich_movies.py --input "D:/Temp/mbdump/tmdb_movies.csv"

Output:
- D:/Temp/mbdump/tmdb_enriched_movies.csv
"""

import pandas as pd
import requests
import time
import argparse

API_KEY = '8289cf63ae0018475953afaf51ce5464'
GENRES_URL = 'https://api.themoviedb.org/3/genre/movie/list'
MOVIE_URL = 'https://api.themoviedb.org/3/movie/{}'
DEFAULT_INPUT = 'D:/Temp/mbdump/tmdb_movies.csv'
OUTPUT_PATH = 'D:/Temp/mbdump/tmdb_enriched_movies.csv'

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, default=DEFAULT_INPUT, help='Path to input CSV containing TMDb movie IDs')
args = parser.parse_args()

def get_genre_lookup():
    r = requests.get(GENRES_URL, params={'api_key': API_KEY})
    genre_data = r.json().get('genres', [])
    return {g['id']: g['name'] for g in genre_data}

def fetch_movie_details(movie_id):
    url = MOVIE_URL.format(movie_id)
    r = requests.get(url, params={'api_key': API_KEY})
    if r.status_code == 200:
        return r.json()
    return None

def main():
    df = pd.read_csv(args.input)
    genre_lookup = get_genre_lookup()
    enriched = []

    total = len(df)
    start_time = time.time()

    for idx, row in df.iterrows():
        movie_id = row['id']
        title = row['title']
        print(f"🔍 [{idx + 1}/{total}] Fetching TMDb ID {movie_id} – {title}")
        try:
            data = fetch_movie_details(movie_id)
            if data:
                genres = [genre_lookup.get(g['id'], '') for g in data.get('genres', [])]
                enriched.append({
                    'input_title': title,
                    'input_year': row['release_date'][:4] if pd.notna(row['release_date']) else '',
                    'tmdb_title': data.get('title'),
                    'tmdb_year': data.get('release_date'),
                    'media_type': 'movie',
                    'tmdb_id': data.get('id'),
                    'popularity': data.get('popularity'),
                    'fuzzy_score': '',  # placeholder
                    'genres': ', '.join(genres) if genres else 'Unknown'
                })
        except Exception as e:
            print(f'⚠️ Error fetching TMDb ID {movie_id}: {e}')
        time.sleep(0.3)

    pd.DataFrame(enriched).to_csv(OUTPUT_PATH, index=False)
    elapsed = time.time() - start_time
    print(f'✅ Enriched data saved to {OUTPUT_PATH}')
    print(f'⏱️ Completed in {elapsed:.2f} seconds.')

if __name__ == '__main__':
    main()
