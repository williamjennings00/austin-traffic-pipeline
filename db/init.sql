CREATE TABLE IF NOT EXISTS traffic_incidents (
    traffic_report_id TEXT PRIMARY KEY,
    published_date TIMESTAMPTZ,
    issue_reported TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    address TEXT,
    traffic_report_status TEXT,
    agency TEXT
);