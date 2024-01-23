import abc


class BaseQuery(abc.ABC):
    @abc.abstractmethod
    def query(self):
        pass
