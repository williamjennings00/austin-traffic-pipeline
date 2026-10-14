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

CREATE TABLE IF NOT EXISTS weather_hourly (
    timestamp TIMESTAMP PRIMARY KEY,
    temperature_2m DOUBLE PRECISION,
    relative_humidity_2m DOUBLE PRECISION,
    precipitation DOUBLE PRECISION,
    wind_speed_10m DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS construction_zones (
    data_source_id TEXT PRIMARY KEY,
    road_names TEXT,
    direction TEXT,
    description TEXT,
    start_date TIMESTAMPTZ,
    end_date TIMESTAMPTZ,
    is_start_date_verified BOOLEAN,
    is_end_date_verified BOOLEAN,
    are_workers_present BOOLEAN,
    work_zone_type TEXT,
    vehicle_impact TEXT,
    critical_corridor TEXT,
    geometry JSONB
);