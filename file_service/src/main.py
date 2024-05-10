import logging
from contextlib import asynccontextmanager

import aiohttp
import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from miniopy_async import Minio
from redis.asyncio import Redis
from src.api.v1 import files, healthcheck
from src.core.config import settings
from src.core.logger import setup_root_logger
from src.db import redis
from src.dependencies.main import setup_dependencies
from src.middleware.main import setup_middleware
from src.storage import minio, session_client

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

setup_root_logger()


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    minio.minio_client = Minio(
        endpoint=settings.endpoint,
        access_key=settings.access_key,
        secret_key=settings.secret_key,
        secure=False,
    )
    session_client.client_session = aiohttp.ClientSession()
    yield
    await redis.redis.close()
    await session_client.client_session.close()


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    docs_url="/api/files/openapi",
    openapi_url="/api/files/openapi.json",
    default_response_class=ORJSONResponse,
    version=settings.version,
    lifespan=lifespan,
)

app.include_router(files.router, prefix="/api/v1/files", tags=["Файлы"])
app.include_router(healthcheck.router, tags=["Heathcheck"])

setup_middleware(app)
setup_dependencies(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level=logging.INFO,
    )
