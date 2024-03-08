from dataclasses import dataclass
from uuid import UUID

from src.app.schemas.events import ContentTypeEnum


@dataclass
class KafkaEvent:
    user_id: str


@dataclass
class KafkaClickedEvent(KafkaEvent):
    type: ContentTypeEnum


@dataclass
class KafkaSeenPageEvent(KafkaEvent):
    url: str
    duration: int


@dataclass
class KafkaVideoQualityEvent(KafkaEvent):
    old_quality: str
    new_quality: str


@dataclass
class KafkaFilmViewCompletedEvent(KafkaEvent):
    film_id: UUID


@dataclass
class KafkaFilteredEvent(KafkaEvent):
    filtered_by: str
