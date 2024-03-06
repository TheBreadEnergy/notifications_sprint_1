from enum import IntEnum

from marshmallow import fields
from src.app import ma_app


class ContentTypeEnum(IntEnum):
    film = 0
    genre = 1
    actor = 2
    trailer = 3
    other = 4


class UserClickedEventSchema(ma_app.Schema):
    timestamp = fields.DateTime(required=True, description="Дата наступления события")
    type = fields.Enum(ContentTypeEnum, description="Что было кликнуто", required=True)


class UserSeenPageEventSchema(ma_app.Schema):
    timestamp = fields.DateTime(required=True, description="Дата наступления события")
    url = fields.Url(
        required=True, description="Адрес страницы, которую просматривал пользовател"
    )
    duration = fields.TimeDelta(
        required=True,
        description="Сколько времени в секундах провел пользователь на странице",
    )


class ChangedVideoQualityEventSchema(ma_app.Schema):
    old_quality = fields.String(required=True, description="Старое качество видео")
    new_quality = fields.String(required=True, description="Новое качество видео")
    timestamp = fields.DateTime(required=True, description="Дата наступления события")


class FilmViewCompletedEventSchema(ma_app.Schema):
    film_id = fields.UUID(
        required=True, description="ID фильма которое пользователь досмотрел"
    )
    timestamp = fields.DateTime(required=True, description="Дата наступления события")


class UserFilteredEventSchema(ma_app.Schema):
    filter_by = fields.String(
        required=True, description="По чему была осуществлена фильтрация"
    )
    timestamp = fields.DateTime(required=True, description="Дата наступления события")


user_clicked_event_schema = UserClickedEventSchema()
user_seen_page_event_schema = UserSeenPageEventSchema()
changed_video_quality_event_schema = ChangedVideoQualityEventSchema()
film_view_completed_event_schema = FilmViewCompletedEventSchema()
filter_user_event_schema = UserFilteredEventSchema()
