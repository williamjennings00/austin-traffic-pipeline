import json
import time

import requests


base_url = "https://data.austintexas.gov/resource/dx9v-zd7x.json"

limit = 1000
offset = 0
all_records = []

while True:
    url = f"{base_url}?$limit={limit}&$offset={offset}"

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

print(f"Saved {len(all_records)} total traffic records.")