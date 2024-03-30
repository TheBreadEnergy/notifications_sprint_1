CREATE TABLE IF NOT EXISTS film_view_completed_events (
        timestamp TIMESTAMP,
        film_id UUID,
        user_id   VARCHAR(100),
        score INTEGER
    ) ORDER BY timestamp;