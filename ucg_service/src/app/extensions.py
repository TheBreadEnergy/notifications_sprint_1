from confluent_kafka import Producer
from flask_apispec import FlaskApiSpec
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from src.app.services.message_broker import KafkaMessageBrokerService
from src.config import Config

ma_app = Marshmallow()
jwt_app = JWTManager()
docs = FlaskApiSpec()


config = {
    "bootstrap.servers": Config.BOOTSTRAP_SERVERS,
    "retry.backoff.ms": Config.RETRY_BACKOFF_MS,
}
producer = Producer(config)
message_broker = KafkaMessageBrokerService(producer=producer)
