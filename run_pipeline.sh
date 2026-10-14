#!/bin/bash

source venv/bin/activate

python src/ingest.py
python src/transform.py
python src/load.py
