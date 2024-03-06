import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", default="secret")
    JWT_ACCESS_TOKEN_EXPIRES = int(
        os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", default=3600)
    )
    JWT_REFRESH_TOKEN_EXPIRES = int(
        os.environ.get("JWT_REFRESH_TOKEN_EXPIRES", default=3600)
    )
    BOOTSTRAP_SERVERS = os.environ.get(
        "BOOTSTRAP_SERVERS", default="158.160.73.60:9094"
    )
    AUTO_OFFSET_RESET = os.environ.get("AUTO_OFFSET_RESET", default="earliest")
    ENABLE_AUTO_COMMIT = bool(os.environ.get("ENABLE_AUTO_COMMIT", default="False"))
    RETRY_BACKOFF_MS = int(os.environ.get("RETRY_BACKOFF_MS", default=500))
    KAFKA_CLICK_TOPIC = os.environ.get("KAFKA_CLICK_TOPIC", default="click")
    KAFKA_SEEN_TOPIC = os.environ.get("KAFKA_SEEN_TOPIC", default="seen")
    KAFKA_VIDEO_TOPIC = os.environ.get("KAFKA_VIDEO_TOPIC", default="video-quality")
    KAFKA_FILM_TOPIC = os.environ.get("KAFKA_FILM_TOPIC", default="film-view")
    KAFKA_FILTER_TOPIC = os.environ.get("KAFKA_FILTER_TOPIC", default="filter")
