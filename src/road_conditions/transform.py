import json
import logging
import os

import pandas as pd


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


with open("data/raw/road_conditions.json", "r") as file:
    data = json.load(file)

df = pd.DataFrame(data)

columns = [
    "id",
    "sensor_id",
    "location_name",
    "location",
    "timestamp",
    "air_temp_primary",
    "temp_surface",
    "condition_text_measured",
    "friction_value_measured",
    "grip_text",
    "relative_humidity",
    "status_code",
]

df = df[columns]

df["timestamp"] = (
    pd.to_datetime(
        df["timestamp"],
        errors="coerce",
    )
    .dt.tz_localize("America/Chicago")
    .dt.tz_convert("UTC")
)

numeric_columns = [
    "air_temp_primary",
    "temp_surface",
    "friction_value_measured",
    "relative_humidity",
    "status_code",
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce",
    )

# 100.1 is documented as an error value for temperature sensors.
df.loc[df["air_temp_primary"] == 100.1, "air_temp_primary"] = pd.NA
df.loc[df["temp_surface"] == 100.1, "temp_surface"] = pd.NA

df = df.dropna(
    subset=["id", "sensor_id", "timestamp"]
)

df = df.drop_duplicates(
    subset=["id"],
    keep="first",
)

df.to_json(
    "data/processed/road_conditions_clean.json",
    orient="records",
    date_format="iso",
    indent=2,
)

logger.info(
    "Saved %s cleaned road condition records",
    len(df),
)