import json
from logging import Logger
from typing import Any, Dict

import backoff
from redis import Redis
from src.config import APP_SETTINGS, BACKOFF_CONFIG
from src.storage.base_storage import BaseStorage


class RedisStorage(BaseStorage):
    def __init__(
        self, redis_adapter: Redis, logger: Logger, name: str = APP_SETTINGS.root_key
    ):
        self.redis_adapter = redis_adapter
        self._logger = logger
        self._name = name

    @backoff.on_exception(**BACKOFF_CONFIG)
    def retrieve_state(self, default_value: dict = dict()) -> Dict[str, Any]:
        self._logger.info(f"Retrieving state by root key: {self._name} ")
        json_data = self.redis_adapter.get(self._name)
        if json_data:
            data = json.loads(json_data)
            return data
        self._logger.info(f"State is not found. Returns default value: {default_value}")
        return default_value

    @backoff.on_exception(**BACKOFF_CONFIG)
    def save_state(self, state_dict: Dict[str, Any]) -> None:
        state = json.dumps(state_dict)
        self.redis_adapter.set(self._name, state)
        self._logger.info(f"Wrote new state object {state_dict}")
