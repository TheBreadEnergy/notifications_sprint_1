from http import HTTPStatus

import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator
from src.api.v1 import healthcheck, system_notifications, user_notifications
from src.core.config import settings
from src.core.logging import setup_root_logger
from src.core.tracing import configure_tracing
from src.dependencies.main import setup_dependencies
from src.middleware.main import setup_middleware

if not settings.debug:
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )

    setup_root_logger()

if settings.enable_tracer:
    configure_tracing()


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    docs_url="/api/notifications/openapi",
    openapi_url="/api/notifications/openapi.json",
    default_response_class=ORJSONResponse,
    version=settings.version,
)


if settings.enable_tracer:

    @app.middleware("http")
    async def before_request(request: Request, call_next):
        response = await call_next(request)
        request_id = request.headers.get("X-Request-Id")
        if not request_id:
            return ORJSONResponse(
                status_code=HTTPStatus.NOT_FOUND,
                content={"detail": "X-Request-Id is required"},
            )
        return response

    FastAPIInstrumentor.instrument_app(app)


app.include_router(
    user_notifications.router,
    prefix="/api/v1/user-notifications",
    tags=["Пользователи"],
)

app.include_router(
    system_notifications.router,
    prefix="/api/v1/system-notifications",
    tags=["Система"],
)

app.include_router(healthcheck.router, tags=["Health Check"])

setup_middleware(app)
setup_dependencies(app)

Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
    )
