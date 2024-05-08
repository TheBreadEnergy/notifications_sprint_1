from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.request_log import RequestLogMiddleware


def setup_middleware(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLogMiddleware)
