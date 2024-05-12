import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from src.api.v1 import websockets
from src.core.config import settings
from src.core.logger import setup_root_logger
from src.middleware.main import setup_middleware

setup_root_logger()

app = FastAPI(
    title=settings.project_name,
    description=settings.description,
    docs_url="/api/websockets/openapi",
    openapi_url="/api/websockets/openapi.json",
    default_response_class=ORJSONResponse,
    version=settings.version,
)

app.include_router(websockets.router, prefix="/api/v1/websockets", tags=["Вебсокеты"])

setup_middleware(app)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level=logging.INFO,
    )
