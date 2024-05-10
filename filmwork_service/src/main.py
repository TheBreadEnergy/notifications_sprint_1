from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from src.api.v1 import films, genres, healthcheck, persons
from src.core.config import settings
from src.core.logger import setup_root_logger
from src.db import elastic, redis
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
    redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    elastic.es = AsyncElasticsearch(
        hosts=[f"{settings.elastic_host}:{settings.elastic_port}"]
    )
    yield
    await redis.redis.close()
    await elastic.es.close()


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    docs_url="/api/films/openapi",
    openapi_url="/api/films/openapi.json",
    default_response_class=ORJSONResponse,
    version=settings.version,
    lifespan=lifespan,
)

app.include_router(films.router, prefix="/api/v1/films", tags=["Фильмы"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["Жанры"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["Персоны"])

app.include_router(healthcheck.router, tags=["Heathcheck"])

setup_middleware(app)
setup_dependencies(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level,
    )
