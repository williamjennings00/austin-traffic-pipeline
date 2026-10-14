import json
import logging
import os

import pandas as pd


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


with open("data/raw/construction.json", "r") as file:
    data = json.load(file)

df = pd.DataFrame(data)

columns = [
    "data_source_id",
    "road_names",
    "direction",
    "description",
    "start_date",
    "end_date",
    "is_start_date_verified",
    "is_end_date_verified",
    "are_workers_present",
    "work_zone_type",
    "vehicle_impact",
    "critical_corridor",
    "geometry",
]

# Keep only columns that actually exist in the API response.
available_columns = [
    column for column in columns
    if column in df.columns
]

df = df[available_columns]

if "start_date" in df.columns:
    df["start_date"] = pd.to_datetime(
        df["start_date"],
        errors="coerce",
    )

if "end_date" in df.columns:
    df["end_date"] = pd.to_datetime(
        df["end_date"],
        errors="coerce",
    )

if "road_names" in df.columns:
    df["road_names"] = df["road_names"].str.strip()

if "direction" in df.columns:
    df["direction"] = df["direction"].str.strip()

if "description" in df.columns:
    df["description"] = df["description"].str.strip()

if "data_source_id" in df.columns:
    df = df.drop_duplicates(
        subset=["data_source_id"],
        keep="first",
    )

df.to_json(
    "data/processed/construction_clean.json",
    orient="records",
    indent=2,
    date_format="iso",
)

logger.info(
    "Saved %s cleaned construction records",
    len(df),
)