from abc import ABC, abstractmethod


class AbstractProducer(ABC):
    @abstractmethod
    def send(self, *args, **kwargs) -> None:
        pass


class AbstractGetProducer(ABC):

    @abstractmethod
    def get(self, *args, **kwargs) -> None:
        pass


class AbstractSortProducer(AbstractGetProducer):

    @abstractmethod
    def get_sorted(self, *args, **kwargs) -> None:
        pass
