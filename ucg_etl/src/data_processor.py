from src.models.events import (KafkaClickedEvent, KafkaFilmViewCompletedEvent,
                               KafkaFilteredEvent, KafkaSeenPageEvent,
                               KafkaVideoQualityEvent)
from src.schemas.events import ContentTypeEnum


def process_clicked_event(message, timestamp):
    message["type"] = ContentTypeEnum(message["type"])
    event = KafkaClickedEvent(**message)
    return {"timestamp": timestamp, "type": event.type.name, "user_id": event.user_id}


def process_seen_page_event(message, timestamp):
    event = KafkaSeenPageEvent(**message)
    return {"timestamp": timestamp, "url": event.url, "duration": event.duration, "user_id": event.user_id}


def process_video_quality_event(message, timestamp):
    event = KafkaVideoQualityEvent(**message)
    return {"timestamp": timestamp, "old_quality": event.old_quality, "new_quality": event.new_quality,
            "user_id": event.user_id}


def process_film_view_completed_event(message, timestamp):
    event = KafkaFilmViewCompletedEvent(**message)
    return {"timestamp": timestamp, "film_id": event.film_id, "user_id": event.user_id}


def process_filtered_event(message, timestamp):
    event = KafkaFilteredEvent(**message)
    return {"timestamp": timestamp, "filtered_by": event.filtered_by, "user_id": event.user_id}
