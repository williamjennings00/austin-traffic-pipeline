import pandas as pd
import psycopg2


df = pd.read_csv("data/processed/traffic_clean.csv")

connection = psycopg2.connect(
    dbname="austin_traffic"
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

print(f"Loaded {len(df)} traffic records into PostgreSQL.")