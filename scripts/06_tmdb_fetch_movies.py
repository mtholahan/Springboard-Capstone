"""
06_tmdb_fetch_movies.py

Fetches popular movies from The Movie Database (TMDb) API.

- Uses TMDb's /discover/movie endpoint (sorted by popularity)
- Takes `--pages` as a parameter (20 results per page)
- Stores basic metadata (ID, title, release date, popularity) to CSV

Usage:
python 06_tmdb_fetch_movies.py --pages 50

Output:
- D:/Temp/mbdump/tmdb_movies.csv
"""

import requests
import csv
import time
import argparse

API_KEY = '8289cf63ae0018475953afaf51ce5464'
BASE_URL = 'https://api.themoviedb.org/3/discover/movie'
OUTPUT_FILE = 'D:/Temp/mbdump/tmdb_movies.csv'

parser = argparse.ArgumentParser()
parser.add_argument('--pages', type=int, default=50, help='Number of pages to fetch (20 results per page)')
args = parser.parse_args()

def fetch_movies(page):
    params = {
        'api_key': API_KEY,
        'sort_by': 'popularity.desc',
        'include_adult': 'false',
        'include_video': 'false',
        'language': 'en-US',
        'page': page
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()['results']

def main():
    all_movies = []
    for page in range(1, args.pages + 1):
        print(f'📥 Fetching page {page}...')
        try:
            movies = fetch_movies(page)
            for movie in movies:
                all_movies.append({
                    'id': movie['id'],
                    'title': movie['title'],
                    'release_date': movie.get('release_date', ''),
                    'popularity': movie['popularity']
                })
            time.sleep(0.3)
        except Exception as e:
            print(f'⚠️ Error fetching page {page}: {e}')
            break

    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'title', 'release_date', 'popularity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for movie in all_movies:
            writer.writerow(movie)

    print(f'✅ Movies saved to {OUTPUT_FILE}')

if __name__ == '__main__':
    main()
