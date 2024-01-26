import inspect
import re
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRoute
from redis.asyncio import Redis
from src.api.v1 import accounts, roles, users
from src.cli import cli
from src.core.config import settings
from src.db import redis
from src.dependencies.main import setup_dependencies


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.project_name,
        description=settings.description,
        version=settings.version,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    cookie_security_schemes = {
        "AuthJWTCookieAccess": {
            "type": "apiKey",
            "in": "header",
            "name": "X-CSRF-TOKEN",
        },
        "AuthJWTCookieRefresh": {
            "type": "apiKey",
            "in": "header",
            "name": "X-CSRF-TOKEN",
        },
    }
    refresh_token_cookie = {
        "name": "refresh_token_cookie",
        "in": "cookie",
        "required": False,
        "schema": {"title": "refresh_token_cookie", "type": "string"},
    }
    access_token_cookie = {
        "name": "access_token_cookie",
        "in": "cookie",
        "required": False,
        "schema": {"title": "access_token_cookie", "type": "string"},
    }

    if "components" in openapi_schema:
        openapi_schema["components"].update(
            {"securitySchemes": cookie_security_schemes}
        )
    else:
        openapi_schema["components"] = {"securitySchemes": cookie_security_schemes}

    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        endpoint = getattr(route, "endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            # access_token
            if (
                re.search("jwt_required", inspect.getsource(endpoint))
                or re.search("fresh_jwt_required", inspect.getsource(endpoint))
                or re.search("jwt_optional", inspect.getsource(endpoint))
            ):
                try:
                    openapi_schema["paths"][path][method]["parameters"].append(
                        access_token_cookie
                    )
                except Exception:
                    openapi_schema["paths"][path][method].update(
                        {"parameters": [access_token_cookie]}
                    )

                # method GET doesn't need to pass X-CSRF-TOKEN
                if method != "get":
                    openapi_schema["paths"][path][method].update(
                        {"security": [{"AuthJWTCookieAccess": []}]}
                    )

            # refresh_token
            if re.search("jwt_refresh_token_required", inspect.getsource(endpoint)):
                try:
                    openapi_schema["paths"][path][method]["parameters"].append(
                        refresh_token_cookie
                    )
                except Exception:
                    openapi_schema["paths"][path][method].update(
                        {"parameters": [refresh_token_cookie]}
                    )

                # method GET doesn't need to pass X-CSRF-TOKEN
                if method != "get":
                    openapi_schema["paths"][path][method].update(
                        {"security": [{"AuthJWTCookieRefresh": []}]}
                    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


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
app.openapi = custom_openapi


app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["Пользователи"])
app.include_router(roles.router, prefix="/api/v1/roles", tags=["Роли"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Пользователи"])

setup_dependencies(app)

if __name__ == "__main__":
    cli()
