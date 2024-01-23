import logging
from typing import Any, Callable

from fastapi import FastAPI

from .registrator import dependencies_container


def setup_dependencies(app: FastAPI, mapper: dict[Any, Callable] | None = None) -> None:
    if mapper is None:
        mapper = dependencies_container
    for interface, dependency in mapper.items():
        app.dependency_overrides[interface] = dependency
    logging.info("\nDependencies mapping: %s", app.dependency_overrides)
