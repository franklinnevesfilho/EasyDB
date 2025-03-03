from abc import ABC, abstractmethod
from typing import Type, Any


class Adapter(ABC):

    def __init__(self, uri: str) -> None:
        self.uri = uri

    @abstractmethod
    def register_models(self, models: []) -> None:
        pass

    @abstractmethod
    async def add(self, model: Type[Any], instance: Any) -> None:
        pass

    @abstractmethod
    async def get_all(self, model: Type[Any]) -> list[Any] | None:
        pass

    @abstractmethod
    async def get_by(self, model: Type[Any], params: dict) -> list[Any] | None:
        pass

    @abstractmethod
    async def delete(self, model: Type[Any], instance: Any) -> None:
        pass

    @abstractmethod
    async def update(self, model: Type[Any], instance: Any) -> None:
        pass
