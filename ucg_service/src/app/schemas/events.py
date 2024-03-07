from enum import IntEnum

from marshmallow import Schema, fields


class ContentTypeEnum(IntEnum):
    film = 0
    genre = 1
    actor = 2
    trailer = 3
    other = 4


class UserClickedEventSchema(Schema):
    timestamp = fields.DateTime(required=True, description="Дата наступления события")
    type = fields.Enum(ContentTypeEnum, description="Что было кликнуто", required=True)


class UserSeenPageEventSchema(Schema):
    timestamp = fields.DateTime(required=True, description="Дата наступления события")
    url = fields.Url(
        required=True, description="Адрес страницы, которую просматривал пользовател"
    )
    duration = fields.TimeDelta(
        required=True,
        description="Сколько времени в секундах провел пользователь на странице",
    )


class ChangedVideoQualityEventSchema(Schema):
    old_quality = fields.String(required=True, description="Старое качество видео")
    new_quality = fields.String(required=True, description="Новое качество видео")
    timestamp = fields.DateTime(required=True, description="Дата наступления события")


class FilmViewCompletedEventSchema(Schema):
    film_id = fields.UUID(
        required=True, description="ID фильма которое пользователь досмотрел"
    )
    timestamp = fields.DateTime(required=True, description="Дата наступления события")


class UserFilteredEventSchema(Schema):
    filter_by = fields.String(
        required=True, description="По чему была осуществлена фильтрация"
    )
    timestamp = fields.DateTime(required=True, description="Дата наступления события")


user_clicked_event_schema = UserClickedEventSchema()
user_seen_page_event_schema = UserSeenPageEventSchema()
changed_video_quality_event_schema = ChangedVideoQualityEventSchema()
film_view_completed_event_schema = FilmViewCompletedEventSchema()
filter_user_event_schema = UserFilteredEventSchema()
