from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from src.app.services.message_broker import KafkaMessageBrokerService

ma_app = Marshmallow()
jwt_app = JWTManager()
flasgger_app = Swagger()

message_broker: KafkaMessageBrokerService | None = None
