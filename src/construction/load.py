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


with open("data/processed/construction_clean.json", "r") as file:
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
        INSERT INTO construction_zones (
            data_source_id,
            road_names,
            direction,
            description,
            start_date,
            end_date,
            is_start_date_verified,
            is_end_date_verified,
            are_workers_present,
            work_zone_type,
            vehicle_impact,
            critical_corridor,
            geometry
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (data_source_id) DO UPDATE SET
            road_names = EXCLUDED.road_names,
            direction = EXCLUDED.direction,
            description = EXCLUDED.description,
            start_date = EXCLUDED.start_date,
            end_date = EXCLUDED.end_date,
            is_start_date_verified = EXCLUDED.is_start_date_verified,
            is_end_date_verified = EXCLUDED.is_end_date_verified,
            are_workers_present = EXCLUDED.are_workers_present,
            work_zone_type = EXCLUDED.work_zone_type,
            vehicle_impact = EXCLUDED.vehicle_impact,
            critical_corridor = EXCLUDED.critical_corridor,
            geometry = EXCLUDED.geometry;
        """,
        (
            record.get("data_source_id"),
            record.get("road_names"),
            record.get("direction"),
            record.get("description"),
            record.get("start_date"),
            record.get("end_date"),
            record.get("is_start_date_verified"),
            record.get("is_end_date_verified"),
            record.get("are_workers_present"),
            record.get("work_zone_type"),
            record.get("vehicle_impact"),
            record.get("critical_corridor"),
            Json(record.get("geometry"))
            if record.get("geometry") is not None
            else None,
        ),
    )


connection.commit()

cursor.close()
connection.close()

logger.info(
    "Loaded %s construction records into PostgreSQL",
    len(records),
)