from abc import ABC, abstractmethod

class Adapter(ABC):
    @abstractmethod
    def create_table(self, model: type):
        pass

    @abstractmethod
    async def add(self, table: str, data: dict):
        pass

    @abstractmethod
    async def get(self, table: str, query: dict=None):
        pass

    @abstractmethod
    async def update(self, table: str, query: dict, update: dict):
        pass

    @abstractmethod
    async def delete(self, table: str, query: dict):
        pass

    @abstractmethod
    async def execute(self, query: str):
        pass