from src.schemas.events.base import BaseEvent


class UserRegisteredEvent(BaseEvent):
    short_url: str


class UserActivatedEvent(BaseEvent):
    ...
