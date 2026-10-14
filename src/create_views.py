import logging
import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


connection = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD") or None,
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
)

cursor = connection.cursor()

cursor.execute(
    """
    CREATE OR REPLACE VIEW traffic_with_weather AS
    SELECT
        t.traffic_report_id,
        t.published_date,
        t.issue_reported,
        t.latitude,
        t.longitude,
        t.address,
        t.traffic_report_status,
        t.agency,
        w.temperature_2m,
        w.relative_humidity_2m,
        w.precipitation,
        w.wind_speed_10m
    FROM traffic_incidents t
    LEFT JOIN weather_hourly w
        ON DATE_TRUNC('hour', t.published_date) = w.timestamp;
    """
)

connection.commit()

cursor.close()
connection.close()

logger.info("Created traffic_with_weather view")