from typing import Any

from src.logger import logger
from src.storage.base_storage import BaseStorage


class State:
    """Класс для работы с состояниями"""

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        state = self.storage.retrieve_state()
        state[key] = value
        self.storage.save_state(state)
        logger.info("State of the object by key %s was changed to %s", key, value)

    def get_state(self, key: str) -> Any:
        value = self.storage.retrieve_state().get(key)
        logger.info("State of the object by key %s was requested", key)
        return value
