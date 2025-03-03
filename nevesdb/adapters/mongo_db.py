from .adapter import Adapter

class MongoAdapter(Adapter):

    def register_model(self, model: type):
        pass

    async def add(self, table: str, data: dict):
        pass

    async def get(self, table: str, query: dict = None):
        pass

    async def update(self, table: str, query: dict, update: dict):
        pass

    async def delete(self, table: str, query: dict):
        pass

    async def execute(self, query: str):
        pass