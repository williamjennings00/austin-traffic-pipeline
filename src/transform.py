import pandas as pd


df = pd.read_json("data/raw/traffic.json")

df = df[
    [
        "traffic_report_id",
        "published_date",
        "issue_reported",
        "latitude",
        "longitude",
        "address",
        "traffic_report_status",
        "agency",
    ]
]

df["agency"] = df["agency"].str.strip()

df["published_date"] = pd.to_datetime(
    df["published_date"],
    errors="coerce",
)

df["issue_reported"] = (
    df["issue_reported"]
    .str.strip()
    .str.upper()
)

df["issue_reported"] = df["issue_reported"].replace({
    "ZSTALLED VEHICLE": "STALLED VEHICLE",
})

df["latitude"] = pd.to_numeric(
    df["latitude"],
    errors="coerce",
)

df["longitude"] = pd.to_numeric(
    df["longitude"],
    errors="coerce",
)

df = df[df["latitude"].between(-90, 90)]
df = df[df["longitude"].between(-180, 180)]

df.to_csv(
    "data/processed/traffic_clean.csv",
    index=False,
)

print(df.head())
print(f"Saved {len(df)} cleaned traffic records.")