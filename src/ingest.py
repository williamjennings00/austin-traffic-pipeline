import json
import logging
import os
import time

import psycopg2
import requests


logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

base_url = "https://data.austintexas.gov/resource/dx9v-zd7x.json"

connection = psycopg2.connect(
    dbname="austin_traffic"
)

cursor = connection.cursor()

cursor.execute(
    "SELECT MAX(published_date) FROM traffic_incidents;"
)

latest_date = cursor.fetchone()[0]
logger.info(
    "Starting traffic ingestion; latest stored published_date: %s",
    latest_date,
)

cursor.close()
connection.close()

limit = 1000
offset = 0
all_records = []

while True:
    if latest_date:
        latest_date_str = latest_date.isoformat()

        url = (
            f"{base_url}"
            f"?$limit={limit}"
            f"&$offset={offset}"
            f"&$where=published_date > '{latest_date_str}'"
        )
    else:
        url = (
            f"{base_url}"
            f"?$limit={limit}"
            f"&$offset={offset}"
        )

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            batch = response.json()
            break

        except requests.RequestException as error:
            logger.warning(
                "Request failed at offset %s (attempt %s/3): %s",
                offset,
                attempt + 1,
                error,
            )

            if attempt == 2:
                raise

            logger.info("Retrying request in 5 seconds")
            time.sleep(5)

    if not batch:
        break

    all_records.extend(batch)

    logger.info("Fetched %s records at offset %s", len(batch), offset)

    offset += limit

with open("data/raw/traffic.json", "w") as file:
    json.dump(all_records, file, indent=2)

logger.info("Saved %s new traffic records to data/raw/traffic.json", len(all_records))
