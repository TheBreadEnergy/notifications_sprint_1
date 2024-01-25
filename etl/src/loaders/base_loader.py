import abc
from typing import Any

from src.config import APP_SETTINGS


class BaseLoader(abc.ABC):
    """Абстрактный класс для пакетной загрузки данных в хранилище.

    Позволяет загружать пакетами данные в выбранное хранилище данных.
    Способ загрузки данных варьируется в зависимости от хранилища
    """

    @abc.abstractmethod
    def load_batch(
        self, items: list[dict[str, Any]], batch_size: int = APP_SETTINGS.batch_size
    ) -> int:
        """
        Осуществляет запись пакета данных указанного размера
        в выбранное хранилище данных.
        :param items: Вставляемые данные
        :param batch_size: размер пакета данных, загружаемых в хранилище
        :return: Число добавленных строк
        """
        pass
