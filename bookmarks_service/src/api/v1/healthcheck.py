from http import HTTPStatus

from fastapi import APIRouter
from src.schema.healthcheck import HealthcheckSchema

router = APIRouter()


@router.get("/healthcheck", description="Perform healthcheck of service")
async def healthcheck():
    return HealthcheckSchema(code=HTTPStatus.OK)
