import abc

from src.config import APP_SETTINGS


class BaseFetcher(abc.ABC):
    """Абстрактный класс для извлечения данных из хранилища данных.

    Позволяет получать пакетами данные из выбранного источника хранения данных.
    Способ получения данных может варироваться от базы данных с которой мы работаем
    """

    @abc.abstractmethod
    def fetch_many(
        self, query: str, size: int = APP_SETTINGS.batch_size, *args, **kwargs
    ):
        pass
