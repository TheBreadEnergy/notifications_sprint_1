import inspect
import os
import re
from contextlib import asynccontextmanager
from http import HTTPStatus

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis
from src.api.v1 import accounts, roles, socials, users
from src.cli import cli
from src.core.config import settings
from src.core.logging import setup_root_logger
from src.middleware.main import setup_middleware
from src.core.tracing import configure_tracing
from src.db import redis
from src.dependencies.main import setup_dependencies

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

setup_root_logger()

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
    if settings.enable_limiter:
        await FastAPILimiter.init(redis.redis)
    yield
    await redis.redis.close()


if settings.enable_tracer:
    configure_tracing()

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

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(settings.base_dir, "static")),
    name="static",
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


app.include_router(accounts.router, prefix="/api/v1/accounts", tags=["Пользователи"])
app.include_router(roles.router, prefix="/api/v1/roles", tags=["Роли"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Пользователи"])
app.include_router(socials.router, prefix="/api/v1/socials", tags=["OAuth2"])

setup_middleware(app)
setup_dependencies(app)

if __name__ == "__main__":
    cli()
