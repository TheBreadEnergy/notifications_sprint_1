import dataclasses
import json

from flask import jsonify, request
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
    changed_video_quality_event_schema,
    film_view_completed_event_schema,
    filter_user_event_schema,
    user_clicked_event_schema,
    user_seen_page_event_schema,
)
from src.app.utilities import serialize_datetime
from src.config import Config


@blueprint.route("/click", methods=["POST"])
@jwt_required()
def process_click_event():
    data = request.get_json()
    user = get_jwt_identity()
    event = user_clicked_event_schema.load(data)
    message = KafkaClickedEvent(
        user_id=user, timestamp=event["timestamp"], type=event["type"]
    )
    message_broker.publish(
        topic=Config.KAFKA_CLICK_TOPIC,
        key=user,
        message=json.dumps(dataclasses.asdict(message), default=serialize_datetime),
    )
    return jsonify(data), 200


@blueprint.route("/seen-pages", methods=["POST"])
@jwt_required()
def process_seen_pages():
    data = request.get_json()
    user = get_jwt_identity()
    event = user_seen_page_event_schema.load(data)
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
    return jsonify(data), 200


@blueprint.route("/video-quality", methods=["POST"])
@jwt_required()
def process_video_quality():
    data = request.get_json()
    user = get_jwt_identity()
    event = changed_video_quality_event_schema.load(data=data)
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
    return jsonify(data), 200


@blueprint.route("/film-view", methods=["POST"])
@jwt_required()
def process_film_view():
    data = request.get_json()
    user = get_jwt_identity()
    event = film_view_completed_event_schema.load(data=data)
    message = KafkaFilmViewCompletedEvent(
        user_id=user, timestamp=event["timestamp"], film_id=event["film_id"]
    )
    message_broker.publish(
        Config.KAFKA_FILM_TOPIC,
        key=user,
        message=json.dumps(dataclasses.asdict(message), default=serialize_datetime),
    )
    return jsonify(data), 200


@blueprint.route("/filter", methods=["POST"])
@jwt_required()
def process_filter():
    data = request.get_json()
    user = get_jwt_identity()
    event = filter_user_event_schema.load(data=data)
    message = KafkaFilteredEvent(
        user_id=user, timestamp=event["timestamp"], filtered_by=event["filter_by"]
    )
    message_broker.publish(
        Config.KAFKA_FILTER_TOPIC,
        key=user,
        message=json.dumps(dataclasses.asdict(message), default=serialize_datetime),
    )
    return jsonify(data), 200
