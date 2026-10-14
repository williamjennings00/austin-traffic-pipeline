-- Top incident types
SELECT
    issue_reported,
    COUNT(*) AS incident_count
FROM traffic_incidents
GROUP BY issue_reported
ORDER BY incident_count DESC
LIMIT 10;


-- Incidents by hour of day
SELECT
    EXTRACT(HOUR FROM published_date)::INTEGER AS hour_of_day,
    COUNT(*) AS incident_count
FROM traffic_incidents
GROUP BY hour_of_day
ORDER BY hour_of_day;


-- Incidents by day of week
SELECT
    EXTRACT(DOW FROM published_date)::INTEGER AS day_number,
    TO_CHAR(published_date, 'Day') AS day_of_week,
    COUNT(*) AS incident_count
FROM traffic_incidents
GROUP BY day_number, day_of_week
ORDER BY day_number;


-- Top incident addresses
SELECT
    address,
    COUNT(*) AS incident_count
FROM traffic_incidents
WHERE address IS NOT NULL
GROUP BY address
ORDER BY incident_count DESC
LIMIT 20;


-- Monthly incident trend
SELECT
    DATE_TRUNC('month', published_date) AS month,
    COUNT(*) AS incident_count
FROM traffic_incidents
GROUP BY month
ORDER BY month;