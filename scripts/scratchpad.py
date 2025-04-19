import pandas as pd
from config import BASE_DIR

JOIN_FILE = BASE_DIR / "data" / "musicbrainz_raw" / "release_group_secondary_type_join"

df = pd.read_csv(
    JOIN_FILE,
    sep="\t",
    header=None,
    names=["release_group", "secondary_type"],
    dtype=str
)

print("🔢 Total rows:", len(df))
print("🎟 Top 10 unique secondary_type IDs:", df["secondary_type"].unique()[:10])
print("🔍 Any matches to '2' (soundtrack)?", '2' in df["secondary_type"].unique())
print(df.sample(5, random_state=42))
