from clickhouse_driver import Client
from src.core.config import settings


class ClickHouseClient:
    def __init__(self):
        self.client = Client(host=settings.CH_HOST, port=settings.CH_PORT)

    def insert_clicked_event(self, data):
        self.client.execute(
            "INSERT INTO user_clicked_events (timestamp, type, user_id) VALUES", [data]
        )

    def insert_seen_page_event(self, data):
        self.client.execute(
            "INSERT INTO user_seen_page_events (timestamp, url, duration, user_id) VALUES",
            [data],
        )

    def insert_video_quality_event(self, data):
        self.client.execute(
            "INSERT INTO changed_video_quality_events (timestamp, old_quality, new_quality, user_id) VALUES",
            [data],
        )

    def insert_film_view_completed_event(self, data):
        self.client.execute(
            "INSERT INTO film_view_completed_events (timestamp, film_id, user_id) VALUES",
            [data],
        )

    def insert_filtered_event(self, data):
        self.client.execute(
            "INSERT INTO user_filtered_events (timestamp, filter_by, user_id) VALUES",
            [data],
        )
