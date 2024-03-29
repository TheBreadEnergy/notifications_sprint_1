import logging
from typing import Any, Callable

from fastapi import FastAPI
from src.dependencies.registrator import dependencies


def setup_dependencies(app: FastAPI, mapper: dict[Any, Callable] | None = None) -> None:
    if mapper is None:
        mapper = dependencies
    for interface, dependency in mapper.items():
        app.dependency_overrides[interface] = dependency
    logging.info("\nDependencies mapping: %s", app.dependency_overrides)
