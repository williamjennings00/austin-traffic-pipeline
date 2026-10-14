import os
from pathlib import Path

import pandas as pd
import psycopg2
from dotenv import load_dotenv


load_dotenv()

connection = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD") or None,
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", "5432"),
)

sql_dir = Path("sql")
reports_dir = Path("reports")

reports_dir.mkdir(exist_ok=True)

cursor = connection.cursor()

for sql_file in sql_dir.glob("*.sql"):
    query = sql_file.read_text()

    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [column.name for column in cursor.description]

    df = pd.DataFrame(rows, columns=columns)

    report_name = sql_file.stem

    print(f"\n--- {report_name} ---")
    print(df)

    df.to_csv(
        reports_dir / f"{report_name}.csv",
        index=False,
    )

cursor.close()
connection.close()

print("\nAnalytics complete.")