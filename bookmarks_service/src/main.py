from contextlib import asynccontextmanager
from http import HTTPStatus

import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from motor.motor_asyncio import AsyncIOMotorClient
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_fastapi_instrumentator import Instrumentator
from src.api.v1 import bookmarks, film_likes, healthcheck, reviews
from src.core.config import settings
from src.core.logger import setup_root_logger
from src.core.tracing import configure_tracing
from src.db import mongo
from src.dependencies.main import setup_dependencies
from src.middleware.main import setup_middleware

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

setup_root_logger()


@asynccontextmanager
async def lifespan(_: FastAPI):
    mongo.mongo_client = AsyncIOMotorClient(str(settings.mongo_conn))
    await mongo.init(client=mongo.mongo_client)
    yield
    mongo.mongo_client.close()


def create_app() -> FastAPI:
    if settings.enable_tracer:
        configure_tracing()
    app = FastAPI(
        title=settings.project_name,
        description=settings.description,
        docs_url="/api/bookmarks/openapi",
        openapi_url="/api/bookmarks/openapi.json",
        default_response_class=ORJSONResponse,
        version=settings.version,
        lifespan=lifespan,
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

    app.include_router(bookmarks.router, prefix="/api/v1/bookmarks", tags=["Закладки"])
    app.include_router(
        film_likes.router, prefix="/api/v1/film-likes", tags=["Лайки / Дизлайки"]
    )
    app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["Отзывы"])

    app.include_router(healthcheck.router, tags=["Heathcheck"])

    setup_middleware(app)
    add_pagination(app)
    setup_dependencies(app)
    return app


app = create_app()


@app.exception_handler(Exception)
def custom_exception_handler(_: Request, exc: Exception):
    return ORJSONResponse(content={"detail": str(exc)})


Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level,
        reload=False,
    )
