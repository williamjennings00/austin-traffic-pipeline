#!/bin/bash
set -e

python src/incidents/ingest.py
python src/incidents/transform.py
python src/incidents/validate.py
python src/incidents/load.py

python src/weather/ingest.py
python src/weather/transform.py
python src/weather/load.py

python src/construction/ingest.py
python src/construction/transform.py
python src/construction/load.py

python src/road_conditions/ingest.py
python src/road_conditions/transform.py
python src/road_conditions/load.py

python src/analytics/create_views.py