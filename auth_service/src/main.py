from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from src.api.v1 import accounts, roles, users
from src.cli import cli
from src.core.config import settings
from src.db import redis
from src.dependencies.main import setup_dependencies


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis = Redis(
        host=settings.cache_host, port=settings.cache_port, decode_responses=True
    )
    yield
    await redis.redis.close()


app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    docs_url="/api/auth/openapi",
    openapi_url="/api/auth/openapi.json",
    default_response_class=ORJSONResponse,
    version=settings.version,
    lifespan=lifespan,
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(accounts.router, prefix="/api/v1/account", tags=["Пользователи"])
app.include_router(roles.router, prefix="/api/v1/roles", tags=["Роли"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Пользователи"])

setup_dependencies(app)

if __name__ == "__main__":
    cli()
