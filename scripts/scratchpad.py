import pandas as pd

df = pd.read_csv("D:/Capstone_Staging/data/soundtracks.tsv", sep="\t", names=[
    "release_group_id", "mbid", "title", "release_year", "artist_id", "artist_credit_id",
    "artist_name", "type", "primary_type", "barcode", "dummy_1",
    "dummy_2", "dummy_3", "dummy_4", "dummy_5", "artist_sort_name",
    "dummy_6", "dummy_7", "created", "dummy_8", "artist_gid"
], header=None, dtype=str)

print("Valid 4-digit years:", df['release_year'].str.match(r'^\\d{4}$').sum())
print("Years between 1900–2025:", df['release_year'].astype(str).str.extract(r'(\\d{4})')[0].astype(float).between(1900, 2025).sum())
