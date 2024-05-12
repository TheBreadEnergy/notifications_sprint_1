from flask import Blueprint

blueprint = Blueprint("healthchecks", __name__)


from src.app.healthchecks import routes
