from fastapi import FastAPI
from loguru import logger
from src.middleware.request_log import RequestLogMiddleware
from starlette.middleware.cors import CORSMiddleware


def setup_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(RequestLogMiddleware)
