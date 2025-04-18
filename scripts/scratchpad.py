import pandas as pd
df = pd.read_csv("D:/Capstone_Staging/data/musicbrainz_raw/release_group_soundtracks.tsv", sep="\t")
print(df.columns.tolist())
