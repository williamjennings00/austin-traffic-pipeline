import logging
import os

import pandas as pd

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


df = pd.read_json("data/raw/traffic.json")
input_count = len(df)
logger.info("Loaded %s raw traffic records", input_count)

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

logger.info(
    "Saved %s cleaned traffic records to data/processed/traffic_clean.csv "
    "(%s rows removed)",
    len(df),
    input_count - len(df),
)
