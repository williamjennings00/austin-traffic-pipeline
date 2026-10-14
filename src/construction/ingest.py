import json
import logging
import os

import requests


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


url = "https://data.austintexas.gov/resource/m39r-fuyi.json"

params = {
    "$limit": 5000,
}

response = requests.get(
    url,
    params=params,
    timeout=30,
)

response.raise_for_status()

data = response.json()

with open("data/raw/construction.json", "w") as file:
    json.dump(data, file, indent=2)

logger.info(
    "Saved %s roadway work zone records",
    len(data),
)