#!/bin/bash
set -e

python src/ingest.py
python src/transform.py
python src/validate.py
python src/load.py

python src/ingest_weather.py
python src/transform_weather.py
python src/load_weather.py