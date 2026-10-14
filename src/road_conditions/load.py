import json
import logging
import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import Json


load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


with open("data/processed/road_conditions_clean.json", "r") as file:
    records = json.load(file)


connection = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD") or None,
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
)

cursor = connection.cursor()


for record in records:
    cursor.execute(
        """
        INSERT INTO road_conditions (
            id,
            sensor_id,
            location_name,
            location,
            timestamp,
            air_temp_primary,
            temp_surface,
            condition_text_measured,
            friction_value_measured,
            grip_text,
            relative_humidity,
            status_code
        )
        VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (id) DO NOTHING;
        """,
        (
            record.get("id"),
            record.get("sensor_id"),
            record.get("location_name"),
            Json(record.get("location"))
            if record.get("location") is not None
            else None,
            record.get("timestamp"),
            record.get("air_temp_primary"),
            record.get("temp_surface"),
            record.get("condition_text_measured"),
            record.get("friction_value_measured"),
            record.get("grip_text"),
            record.get("relative_humidity"),
            record.get("status_code"),
        ),
    )


connection.commit()

cursor.close()
connection.close()

logger.info(
    "Loaded %s road condition records into PostgreSQL",
    len(records),
)