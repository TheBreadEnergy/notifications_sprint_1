from flask import Blueprint

blueprint = Blueprint("events", __name__)

from src.app.events.v1 import routes
