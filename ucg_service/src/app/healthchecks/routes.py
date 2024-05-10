from http import HTTPStatus

from flask_apispec import doc, marshal_with
from src.app.healthchecks import blueprint
from src.app.schemas.healthcheck import HealthcheckSchema


@blueprint.route("/healthchecks", methods=["GET"])
@doc(
    description="Health checks",
    summary="Health checks",
    tags=["healthcheck"],
)
@marshal_with(HealthcheckSchema, description="Ответ", code=200)
def healthcheck(*args, **kwargs):
    return {"status": HTTPStatus.OK}, HTTPStatus.OK
