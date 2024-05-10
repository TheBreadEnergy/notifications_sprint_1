import json

from flask import Flask
from marshmallow import ValidationError
from src.app.events.v1.routes import (
    process_click_event,
    process_film_view,
    process_filter,
    process_seen_pages,
    process_video_quality,
)
from src.app.extensions import docs, jwt_app, ma_app
from src.app.healthchecks.routes import healthcheck
from src.app.services.message_broker import KafkaMessageBrokerService
from src.app.swagger import setup_swagger
from src.app.tracing import configure_tracing
from src.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # Initialize flask extensions here
    ma_app.init_app(app)
    jwt_app.init_app(app)
    setup_swagger(docs, app)

    if not Config.DEBUG:
        configure_tracing(app)

    # register blueprints here
    from src.app.events import blueprint as events_blueprint
    from src.app.healthchecks import blueprint as healthchecks_blueprint

    app.register_blueprint(events_blueprint, url_prefix="/api/v1/events")
    app.register_blueprint(healthchecks_blueprint, url_prefix="")

    docs.register(process_click_event, blueprint="events")
    docs.register(process_seen_pages, blueprint="events")
    docs.register(process_video_quality, blueprint="events")
    docs.register(process_film_view, blueprint="events")
    docs.register(process_filter, blueprint="events")
    docs.register(healthcheck, blueprint="healthchecks")

    @app.errorhandler(ValidationError)
    def register_validation_error(error):
        print(error)
        rv = dict({"message": json.dumps(error.messages)})
        return rv, 422

    return app
