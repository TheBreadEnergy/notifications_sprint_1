import dataclasses
import json

from flask import jsonify
from flask_apispec import doc, marshal_with, use_kwargs
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.app.events import blueprint
from src.app.extensions import message_broker
from src.app.models.events import (
    KafkaClickedEvent,
    KafkaFilmViewCompletedEvent,
    KafkaFilteredEvent,
    KafkaSeenPageEvent,
    KafkaVideoQualityEvent,
)
from src.app.schemas.events import (
    ChangedVideoQualityEventSchema,
    FilmViewCompletedEventSchema,
    UserClickedEventSchema,
    UserFilteredEventSchema,
    UserSeenPageEventSchema,
)
from src.app.utilities import serialize_datetime
from src.config import Config


@blueprint.route("/clicks", methods=["POST"])
@doc(
    description="Обработка событий связанных с кликами",
    summary="Обработка событий связанных с кликами",
    tags=["events"],
)
@jwt_required()
@use_kwargs(UserClickedEventSchema)
@marshal_with(UserClickedEventSchema, description="Отправленное событие", code=200)
@marshal_with(None, description="Ошибка валидации.", code=422)
def process_click_event(**event):
    user = get_jwt_identity()
    message = KafkaClickedEvent(
        user_id=user, timestamp=event["timestamp"], type=event["type"]
    )
    message_broker.publish(
        topic=Config.KAFKA_CLICK_TOPIC,
        key=user,
        message=json.dumps(dataclasses.asdict(message), default=serialize_datetime),
    )
    return jsonify(event), 200


@blueprint.route("/seen-pages", methods=["POST"])
@jwt_required()
@use_kwargs(UserSeenPageEventSchema)
@marshal_with(UserSeenPageEventSchema, description="Отправленное событие", code=200)
@marshal_with(None, description="Ошибка валидации.", code=422)
@doc(
    description="Обработка событий связанных с просмотром страниц",
    summary="Обработка событий связанных с просмотром страниц",
    tags=["events"],
)
def process_seen_pages(**event):
    user = get_jwt_identity()
    message = KafkaSeenPageEvent(
        user_id=user,
        timestamp=event["timestamp"],
        url=event["url"],
        duration=event["duration"],
    )
    message_broker.publish(
        topic=Config.KAFKA_SEEN_TOPIC,
        key=user,
        message=json.dumps(dataclasses.asdict(message), default=serialize_datetime),
    )
    return jsonify(event), 200


@blueprint.route("/video-quality", methods=["POST"])
@jwt_required()
@use_kwargs(ChangedVideoQualityEventSchema)
@marshal_with(
    ChangedVideoQualityEventSchema, description="Отправленное событие", code=200
)
@marshal_with(None, description="Ошибка валидации.", code=422)
@doc(
    description="Обработка событий связанных с изменением качества видео",
    summary="Обработка событий связанных с изменением качества видео",
    tags=["events"],
)
def process_video_quality(**event):
    user = get_jwt_identity()
    message = KafkaVideoQualityEvent(
        user_id=user,
        timestamp=event["timestamp"],
        old_quality=event["old_quality"],
        new_quality=event["new_quality"],
    )
    message_broker.publish(
        topic=Config.KAFKA_VIDEO_TOPIC,
        key=user,
        message=json.dumps(dataclasses.asdict(message), default=serialize_datetime),
    )
    return jsonify(event), 200


@blueprint.route("/film-view", methods=["POST"])
@jwt_required()
@use_kwargs(FilmViewCompletedEventSchema)
@marshal_with(
    FilmViewCompletedEventSchema, description="Отправленное событие", code=200
)
@marshal_with(None, description="Ошибка валидации.", code=422)
@doc(
    description="Обработка событий связанных с просмотром до конца фильма",
    summary="Обработка событий связанных с просмотром до конца фильма",
    tags=["events"],
)
def process_film_view(**event):
    user = get_jwt_identity()
    message = KafkaFilmViewCompletedEvent(
        user_id=user, timestamp=event["timestamp"], film_id=event["film_id"]
    )
    message_broker.publish(
        Config.KAFKA_FILM_TOPIC,
        key=user,
        message=json.dumps(dataclasses.asdict(message), default=serialize_datetime),
    )
    return jsonify(event), 200


@blueprint.route("/filter", methods=["POST"])
@jwt_required()
@use_kwargs(UserFilteredEventSchema)
@marshal_with(UserFilteredEventSchema, description="Отправленное событие", code=200)
@marshal_with(None, description="Ошибка валидации.", code=422)
@doc(
    description="Обработка событий связанных с фильтрацией контента",
    summary="Обработка событий связанных с фильтрацией контента",
    tags=["events"],
)
def process_filter(**event):
    user = get_jwt_identity()
    message = KafkaFilteredEvent(
        user_id=user, timestamp=event["timestamp"], filtered_by=event["filter_by"]
    )
    message_broker.publish(
        Config.KAFKA_FILTER_TOPIC,
        key=user,
        message=json.dumps(dataclasses.asdict(message), default=serialize_datetime),
    )
    return jsonify(event), 200
