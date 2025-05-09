import pandas as pd
from pathlib import Path
import re

INPUT_PATH = Path("D:/Capstone_Staging/data/soundtracks.tsv")
OUTPUT_PATH = Path("D:/Capstone_Staging/data/tmdb_input_candidates.csv")

# Update column names based on actual TSV structure
col_names = [
    "release_group_id", "mbid", "title", "release_year", "artist_id", "artist_credit_id",
    "artist_name", "type", "primary_type", "barcode", "dummy_1",
    "dummy_2", "dummy_3", "dummy_4", "dummy_5", "artist_sort_name",
    "dummy_6", "dummy_7", "created", "dummy_8", "artist_gid"
]

def normalize_title(title):
    # Lowercase, remove special characters, strip
    return re.sub(r"[^a-z0-9\s]", "", title.lower()).strip()

def extract_year(value):
    match = re.match(r'^(\d{4})', str(value))
    return int(match.group(1)) if match else None

def main():
    print("Loading filtered soundtracks...")
    df = pd.read_csv(INPUT_PATH, sep="\t", names=col_names, header=None, dtype=str)

    print(f"Initial row count: {len(df):,}")
    df = df[['title', 'release_year']].dropna()
    df = df.rename(columns={'title': 'release_group_name', 'release_year': 'year'})

    df['year'] = df['year'].apply(extract_year)
    df = df.dropna(subset=['year'])
    df['year'] = df['year'].astype(int)
    df = df[df['year'].between(1900, 2025)]

    df['normalized_title'] = df['release_group_name'].apply(normalize_title)
    df = df[df['normalized_title'].str.len() >= 3]

    df = df[['normalized_title', 'year']].drop_duplicates()
    df = df.sort_values(['year', 'normalized_title'])

    print(f"Output row count: {len(df):,}")
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
