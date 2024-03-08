CREATE TABLE user_clicked_events
(
    timestamp DateTime,
    type      Enum('film' = 0, 'genre' = 1, 'actor' = 2, 'trailer' = 3, 'other' = 4),
    user_id   String
) ENGINE = MergeTree()
ORDER BY timestamp;

CREATE TABLE user_seen_page_events
(
    timestamp DateTime,
    url       String,
    duration  UInt32,
    user_id   String
) ENGINE = MergeTree()
ORDER BY timestamp;

CREATE TABLE changed_video_quality_events
(
    timestamp   DateTime,
    old_quality String,
    new_quality String,
    user_id     String
) ENGINE = MergeTree()
ORDER BY timestamp;

CREATE TABLE film_view_completed_events
(
    timestamp DateTime,
    film_id   UUID,
    user_id   String
) ENGINE = MergeTree()
ORDER BY timestamp;


CREATE TABLE user_filtered_events
(
    timestamp DateTime,
    filter_by String,
    user_id   String
) ENGINE = MergeTree()
ORDER BY timestamp;
