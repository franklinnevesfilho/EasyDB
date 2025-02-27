from easydata.core.adapters import adapters
from easydata.core.adapter import Adapter
from easydata.core import logger

_compatible_dbs = {
    "sqlite": "sqlite:///{db_url}/{db_name}.db",
    "postgresql": "postgresql://{db_user}:{db_password}@{db_url}/{db_name}",
    "mysql": "mysql://{db_user}:{db_password}@{db_url}/{db_name}",
    "mongodb": "mongodb://{db_user}:{db_password}@{db_url}/{db_name}",
}
def _get_db(db_type, db_user: str, db_password: str, db_name: str, db_url: str):
    """
    Returns the database object for the given database type.
    """
    if db_type not in _compatible_dbs:
        message = f"Database type {db_type} is not supported."
        logger.error(message)
        raise ValueError(message)

    db_uri = _compatible_dbs[db_type].format(db_user=db_user, db_password=db_password, db_name=db_name, db_url=db_url)
    db_adapter = adapters[db_type](db_uri)

    return db_adapter


class EasyData:
    def __init__(self, db_user:str, db_password, db_name:str, db_url: str, db_type: str):
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.db_url = db_url
        self.db_type = db_type

        self.db: Adapter = _get_db(db_type, db_user, db_password, db_name, db_url)

    def register_models(self, models: list):
        """register models to database"""
        for model in models:
            self.db.create_table(model)
            logger.info(f"Model `{model.__name__}` is ready.")
        logger.info("All models are ready.")

    async def add(self, instance):
        """add model instance to database"""
        return await self.db.create(instance.__class__.__name__.lower(), instance.to_dict())

    async def get(self, model, query: dict):
        """get model instance from database"""
        return await self.db.get(model.__name__.lower(), query)

    async def update(self, model, query: dict, update: dict):
        """update model instance in database"""
        return await self.db.update(model.__name__.lower(), query, update)

    async def delete(self, model, query: dict):
        """delete model instance from database"""
        return await self.db.delete(model.__name__.lower(), query)



