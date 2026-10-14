import json
import requests


base_url = "https://data.austintexas.gov/resource/dx9v-zd7x.json"

limit = 1000
offset = 0
all_records = []

while True:
    url = f"{base_url}?$limit={limit}&$offset={offset}"

    response = requests.get(url)
    response.raise_for_status()

    batch = response.json()

    if not batch:
        break

    all_records.extend(batch)

    print(f"Fetched {len(batch)} records at offset {offset}")

    offset += limit

with open("data/raw/traffic.json", "w") as file:
    json.dump(all_records, file, indent=2)

print(f"Saved {len(all_records)} total traffic records.")