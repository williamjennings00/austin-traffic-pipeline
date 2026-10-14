import json
import logging
import os

import requests


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 30.2672,
    "longitude": -97.7431,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
    ],
    "past_days": 7,
    "forecast_days": 1,
    "timezone": "America/Chicago",
}

response = requests.get(
    url,
    params=params,
    timeout=30,
)

response.raise_for_status()

data = response.json()

with open("data/raw/weather.json", "w") as file:
    json.dump(data, file, indent=2)

logger.info(
    "Saved %s hourly weather records",
    len(data["hourly"]["time"]),
)