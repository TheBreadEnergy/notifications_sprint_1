CREATE TABLE IF NOT EXISTS film_view_completed_events (
        timestamp TIMESTAMP,
        film_id   UUID,
        user_id   String,
        score UInt32,
    ) Engine=MergeTree() ORDER BY timestamp;