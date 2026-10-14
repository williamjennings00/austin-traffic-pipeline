#!/bin/bash
set -e

python src/ingest.py
python src/transform.py
python src/validate.py
python src/load.py