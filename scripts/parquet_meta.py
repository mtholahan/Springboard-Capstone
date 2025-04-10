import pandas as pd
df = pd.read_parquet("D:/Temp/mbdump/soundtracks.parquet")
print(df.columns.tolist())
