import json

from confluent_kafka import Producer
from flask import Flask
from flask_request_id_header.middleware import RequestID
from marshmallow import ValidationError
from src.app.extensions import flasgger_app, jwt_app, ma_app
from src.app.services.message_broker import KafkaMessageBrokerService
from src.app.tracing import configure_tracing
from src.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    config = {
        "bootstrap.servers": Config.BOOTSTRAP_SERVERS,
        "retry.backoff.ms": Config.RETRY_BACKOFF_MS,
    }
    producer = Producer(config)
    extensions.message_broker = KafkaMessageBrokerService(producer=producer)

    # Initialize flask extensions here
    ma_app.init_app(app)
    jwt_app.init_app(app)
    flasgger_app.init_app(app)
    if Config.DEBUG:
        configure_tracing(app)

    # register blueprints here
    from src.app.events import blueprint as events_blueprint

    app.register_blueprint(events_blueprint, url_prefix="/api/v1/events")

    @app.errorhandler(ValidationError)
    def register_validation_error(error):
        rv = dict({"message": json.dumps(error.messages)})
        return rv, 422

    return app
