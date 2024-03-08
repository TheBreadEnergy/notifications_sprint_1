from src.models.events import (
    KafkaClickedEvent,
    KafkaFilmViewCompletedEvent,
    KafkaFilteredEvent,
    KafkaSeenPageEvent,
    KafkaVideoQualityEvent,
)
from src.schemas.events import ContentTypeEnum


def process_clicked_event(message, timestamp):
    message["type"] = ContentTypeEnum(message["type"])
    event = KafkaClickedEvent(**message)
    return (timestamp, event.type.name, event.user_id)


def process_seen_page_event(message, timestamp):
    event = KafkaSeenPageEvent(**message)
    return (timestamp, event.url, event.duration, event.user_id)


def process_video_quality_event(message, timestamp):
    event = KafkaVideoQualityEvent(**message)
    return (timestamp, event.old_quality, event.new_quality, event.user_id)


def process_film_view_completed_event(message, timestamp):
    event = KafkaFilmViewCompletedEvent(**message)
    return (timestamp, event.film_id, event.user_id)


def process_filtered_event(message, timestamp):
    event = KafkaFilteredEvent(**message)
    return (timestamp, event.filtered_by, event.user_id)
