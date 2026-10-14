import json
import time

import psycopg2
import requests


base_url = "https://data.austintexas.gov/resource/dx9v-zd7x.json"

connection = psycopg2.connect(
    dbname="austin_traffic"
)

cursor = connection.cursor()

cursor.execute(
    "SELECT MAX(published_date) FROM traffic_incidents;"
)

latest_date = cursor.fetchone()[0]

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
            print(f"Request failed at offset {offset}: {error}")

            if attempt == 2:
                raise

            print("Retrying in 5 seconds...")
            time.sleep(5)

    if not batch:
        break

    all_records.extend(batch)

    print(f"Fetched {len(batch)} records at offset {offset}")

    offset += limit

with open("data/raw/traffic.json", "w") as file:
    json.dump(all_records, file, indent=2)

print(f"Saved {len(all_records)} new traffic records.")