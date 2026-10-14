import json

import requests


url = "https://data.austintexas.gov/resource/dx9v-zd7x.json?$limit=100"

response = requests.get(url)
response.raise_for_status()

data = response.json()

with open("data/raw/traffic.json", "w") as file:
    json.dump(data, file, indent=2)

print(f"Saved {len(data)} traffic records.")