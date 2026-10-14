#!/bin/bash
set -e

python src/incidents/ingest.py
python src/incidents/transform.py
python src/incidents/validate.py
python src/incidents/load.py

python src/weather/ingest.py
python src/weather/transform.py
python src/weather/load.py

python src/analytics/create_views.py