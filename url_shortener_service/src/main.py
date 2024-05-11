from contextlib import asynccontextmanager
from http import HTTPStatus

import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi_limiter import FastAPILimiter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis
from src.api import healthcheck
from src.api.v1 import links
from src.cache import redis
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


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis = Redis(
        host=settings.cache_host, port=settings.cache_port, decode_responses=True
    )
    if settings.enable_limiter:
        await FastAPILimiter.init(redis.redis)
    yield
    await redis.redis.close()


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    docs_url="/api/link-shortener/openapi",
    openapi_url="/api/link-shortener/openapi.json",
    default_response_class=ORJSONResponse,
    version=settings.version,
    lifespan=lifespan,
)

if settings.enable_tracer:
    configure_tracing()

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


app.include_router(links.router, prefix="/api/v1/link-shortener", tags=["Links"])
app.include_router(healthcheck.router, tags=["Heathcheck"])


setup_middleware(app)
setup_dependencies(app)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
    )
