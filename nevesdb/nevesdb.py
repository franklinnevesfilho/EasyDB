from typing import Type
from .adapters import Adapter
from .logger import logger


class NevesDB:
    def __init__(self, uri: str, adapter: Type[Adapter]):
        self.adapter = adapter(uri=uri)

    def register_models(self, models:[]):
        self.adapter.register_models(models)
        logger.info(f"Registered {len(models)} models")

    async def add(self, model, instance):
        return await self.adapter.add(model, instance)

    async def get_all(self, model):
        return await self.adapter.get_all(model)

    async def get_by(self, model, params: dict):
        return await self.adapter.get_by(model, params)

    async def delete(self, model, instance):
        return await self.adapter.delete(model, instance)

    async def update(self, model, instance):
        return await self.adapter.update(model, instance)
