import json
import logging
import os
from datetime import datetime, timedelta

import requests


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


base_url = "https://data.austintexas.gov/resource/ypbq-i42h.json"

start_time = datetime.utcnow() - timedelta(days=1)

params = {
    "$limit": 50000,
    "$where": f"timestamp >= '{start_time.strftime('%Y-%m-%dT%H:%M:%S')}'",
    "$order": "timestamp ASC",
}

response = requests.get(
    base_url,
    params=params,
    timeout=30,
)

response.raise_for_status()

data = response.json()

with open("data/raw/road_conditions.json", "w") as file:
    json.dump(data, file, indent=2)

logger.info(
    "Saved %s road condition records",
    len(data),
)