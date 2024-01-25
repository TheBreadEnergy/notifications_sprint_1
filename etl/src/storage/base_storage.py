import abc
from typing import Any, Dict


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния

    Позволяет сохранять и получать состояние.
    Способ хранения состояния может варьироваться в зависимости
    от итоговой реализации. Например, можно хранить информацию
    в базе данных или в распределённом файловом хранилище.
    """

    @abc.abstractmethod
    def save_state(self, state_dict: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище"""

    @abc.abstractmethod
    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояния из хранилища"""
        pass
