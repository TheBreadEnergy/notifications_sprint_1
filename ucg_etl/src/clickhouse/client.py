import asyncio

from clickhouse_driver import Client

from src.core.config import settings


class ClickHouseClient:
    def __init__(self):
        self.client = Client(host=settings.CH_HOST, port=settings.CH_PORT)
        self.buffers = {
            'user_clicked_events': [],
            'user_seen_page_events': [],
            'changed_video_quality_events': [],
            'film_view_completed_events': [],
            'user_filtered_events': []
        }
        self.buffer_limit = 1000  # Максимальный размер буфера для каждого типа события
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.flush_buffers_periodically())

        # Маппинг типов событий на соответствующие запросы
        self.query_mapping = {
            'user_clicked_events':
                "INSERT INTO user_clicked_events (timestamp, type, user_id) VALUES",
            'user_seen_page_events':
                "INSERT INTO user_seen_page_events (timestamp, url, duration, user_id) VALUES",
            'changed_video_quality_events':
                "INSERT INTO changed_video_quality_events (timestamp, old_quality, new_quality, user_id) VALUES",
            'film_view_completed_events':
                "INSERT INTO film_view_completed_events (timestamp, film_id, user_id) VALUES",
            'user_filtered_events':
                "INSERT INTO user_filtered_events (timestamp, filtered_by, user_id) VALUES",
        }

    async def flush_buffers_periodically(self):
        while True:
            await asyncio.sleep(5)  # Периодическая отправка каждые 60 секунд
            for event_type in self.buffers.keys():
                if self.buffers[event_type]:
                    await self.flush_buffer(event_type)

    async def flush_buffer(self, event_type):
        data_batch = self.buffers[event_type]
        if not data_batch:
            return

        query = self.query_mapping[event_type]
        self.client.execute(query, data_batch)

        self.buffers[event_type] = []  # Очищаем буфер после отправки

    def add_event(self, event_type, data):
        self.buffers[event_type].append(data)
        if len(self.buffers[event_type]) >= self.buffer_limit:
            asyncio.create_task(self.flush_buffer(event_type))  # Асинхронная отправка при достижении лимита буфера
