import pandas as pd


df = pd.read_csv("data/processed/traffic_clean.csv")

assert df["traffic_report_id"].notna().all()
assert df["traffic_report_id"].is_unique

assert df["published_date"].notna().all()

assert df["latitude"].between(-90, 90).all()
assert df["longitude"].between(-180, 180).all()

print("All data quality checks passed.")