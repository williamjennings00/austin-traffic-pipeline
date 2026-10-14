# Austin Traffic Pipeline

This project ingests Austin traffic incidents, cleans the records, and loads them into PostgreSQL.

## Logging

Each pipeline stage writes timestamped progress and warning messages to standard error using Python logging. The default level is `INFO`. Set the `LOG_LEVEL` environment variable to `DEBUG`, `WARNING`, or another standard Python logging level to adjust verbosity.

Run the stages from the project root:

```sh
python src/ingest.py
python src/transform.py
python src/load.py
```
