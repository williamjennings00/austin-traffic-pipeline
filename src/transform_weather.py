import json
import logging
import os

import pandas as pd


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


with open("data/raw/weather.json", "r") as file:
    data = json.load(file)

hourly = data["hourly"]

df = pd.DataFrame(
    {
        "timestamp": hourly["time"],
        "temperature_2m": hourly["temperature_2m"],
        "relative_humidity_2m": hourly["relative_humidity_2m"],
        "precipitation": hourly["precipitation"],
        "wind_speed_10m": hourly["wind_speed_10m"],
    }
)

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
)

df = df.dropna(subset=["timestamp"])

df.to_csv(
    "data/processed/weather_clean.csv",
    index=False,
)

logger.info(
    "Saved %s cleaned weather records to data/processed/weather_clean.csv",
    len(df),
)