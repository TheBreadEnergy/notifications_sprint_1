from enum import IntEnum

from marshmallow import Schema, fields


class ContentTypeEnum(IntEnum):
    film = 0
    genre = 1
    actor = 2
    trailer = 3
    other = 4


class UserClickedEventSchema(Schema):
    type = fields.Enum(ContentTypeEnum, description="Что было кликнуто", required=True)


class UserSeenPageEventSchema(Schema):
    url = fields.Url(
        required=True, description="Адрес страницы, которую просматривал пользовател"
    )
    duration = fields.Int(
        required=True,
        description="Сколько времени в секундах провел пользователь на странице",
    )


class ChangedVideoQualityEventSchema(Schema):
    old_quality = fields.String(required=True, description="Старое качество видео")
    new_quality = fields.String(required=True, description="Новое качество видео")


class FilmViewCompletedEventSchema(Schema):
    film_id = fields.UUID(
        required=True, description="ID фильма которое пользователь досмотрел"
    )


class UserFilteredEventSchema(Schema):
    filter_by = fields.String(
        required=True, description="По чему была осуществлена фильтрация"
    )


user_clicked_event_schema = UserClickedEventSchema()
user_seen_page_event_schema = UserSeenPageEventSchema()
changed_video_quality_event_schema = ChangedVideoQualityEventSchema()
film_view_completed_event_schema = FilmViewCompletedEventSchema()
filter_user_event_schema = UserFilteredEventSchema()
