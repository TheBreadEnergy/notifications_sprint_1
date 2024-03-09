import json
import logging
from datetime import datetime

from aiokafka import ConsumerRecord

from src.core.config import settings
from src.data_processor import (process_clicked_event,
                                process_film_view_completed_event,
                                process_filtered_event,
                                process_seen_page_event,
                                process_video_quality_event)

logger = logging.getLogger(__name__)


class MessageRouter:
    def __init__(self, clickhouse_client):
        self.clickhouse_client = clickhouse_client
        self.topic_to_process_and_event_type = {
            settings.KAFKA_CLICK_TOPIC: (
                process_clicked_event, 'user_clicked_events'
            ),
            settings.KAFKA_SEEN_TOPIC: (
                process_seen_page_event, 'user_seen_page_events'
            ),
            settings.KAFKA_VIDEO_TOPIC: (
                process_video_quality_event, 'changed_video_quality_events'
            ),
            settings.KAFKA_FILM_TOPIC: (
                process_film_view_completed_event, 'film_view_completed_events'
            ),
            settings.KAFKA_FILTER_TOPIC: (
                process_filtered_event, 'user_filtered_events'
            ),
        }

    async def route_message(self, msg: ConsumerRecord):
        try:
            topic_name = msg.topic
            if topic_name in self.topic_to_process_and_event_type:
                process_function, event_type = self.topic_to_process_and_event_type[topic_name]
                timestamp = datetime.fromtimestamp(msg.timestamp / 1000.0)
                message = json.loads(msg.value.decode("utf-8"))
                data = process_function(message, timestamp)
                self.clickhouse_client.add_event(event_type, data)
            else:
                logger.warning(f"Нет обработчика для топика {topic_name}")
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка декодирования JSON: {e}")
