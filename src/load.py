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


df = pd.read_csv("data/processed/traffic_clean.csv")
logger.info("Loaded %s cleaned traffic records", len(df))

df = df.astype(object).where(pd.notna(df), None)

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
        INSERT INTO traffic_incidents (
            traffic_report_id,
            published_date,
            issue_reported,
            latitude,
            longitude,
            address,
            traffic_report_status,
            agency
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (traffic_report_id) DO NOTHING;
        """,
        (
            row["traffic_report_id"],
            row["published_date"],
            row["issue_reported"],
            row["latitude"],
            row["longitude"],
            row["address"],
            row["traffic_report_status"],
            row["agency"],
        ),
    )

connection.commit()

cursor.close()
connection.close()

logger.info("Loaded %s traffic records into PostgreSQL", len(df))
