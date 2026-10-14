import logging
import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


df = pd.read_csv("data/processed/weather_clean.csv")

connection = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD") or None,
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
)

cursor = connection.cursor()

for _, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO weather_hourly (
            timestamp,
            temperature_2m,
            relative_humidity_2m,
            precipitation,
            wind_speed_10m
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (timestamp) DO NOTHING;
        """,
        (
            row["timestamp"],
            row["temperature_2m"],
            row["relative_humidity_2m"],
            row["precipitation"],
            row["wind_speed_10m"],
        ),
    )

connection.commit()

cursor.close()
connection.close()

logger.info(
    "Loaded %s weather records into PostgreSQL",
    len(df),
)