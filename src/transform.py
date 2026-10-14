import pandas as pd

df = pd.read_json("data/raw/traffic.json")

print(df.head())
print(df.columns)
print(df.dtypes)