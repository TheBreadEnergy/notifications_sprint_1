import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.api.v1 import system_notifications, user_notifications
from src.core.config import settings
from src.dependencies.main import setup_dependencies
from src.middleware.main import setup_middleware

app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    docs_url="/api/notifications/openapi",
    openapi_url="/api/notifications/openapi.json",
    default_response_class=ORJSONResponse,
    version=settings.version,
)


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

setup_middleware(app)
setup_dependencies(app)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
    )
