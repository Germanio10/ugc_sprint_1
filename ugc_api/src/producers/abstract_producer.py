from abc import ABC, abstractmethod


class AbstractProducer(ABC):
    @abstractmethod
    def send(self, *args, **kwargs) -> None:
        pass
