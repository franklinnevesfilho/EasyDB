from typing import Dict, List, Optional, Type, TypeVar, Any
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select  # For async queries

from .adapter import Adapter
from ..model import Model
from ..logger import logger


T = TypeVar('T', bound='Base')

Base = declarative_base()

def _get_base_model(model: Type[Model]) -> Type[Base]:
    """
    Dynamically creates an SQLAlchemy model class based on the provided `Model`.
    """
    attributes: Dict[str, Any] = {
        '__tablename__': model.__name__.lower()
    }

    for key, value in model.__annotations__.items():
        if key == 'id':
            attributes[key] = Column(Integer, primary_key=True, autoincrement=True)
        elif value in [int, str, float]:
            column_type = {int: Integer, str: String(255), float: Float}[value]
            attributes[key] = Column(column_type)
        else:
            raise TypeError(f"Unsupported type {value} for attribute {key} in model {model.__name__}")

    if 'id' not in attributes:
        attributes['id'] = Column(Integer, primary_key=True, autoincrement=True)

    return type(model.__name__, (Base,), attributes)


class SQLAdapter(Adapter):
    def __init__(self, uri: str, echo: bool = False) -> None:
        super().__init__(uri)
        self.engine = create_async_engine(self.uri, echo=echo)
        self.Session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
        self.model_classes = {}

    def register_models(self, models: List[Type[Model]]) -> None:
        """
        Register the models with the database. This creates tables if they don't exist.
        """
        for model in models:
            base_model = _get_base_model(model)
            self.model_classes[model.__name__] = base_model
        # Ensure tables are created in the database
        Base.metadata.create_all(self.engine)

    async def add(self, model: Type[Base], instance: Any) -> None:
        """
        Add a new instance of the model to the database.
        """
        async with self.Session() as session:
            async with session.begin():  # Ensure a proper transaction begins
                session.add(instance)
                await session.commit()

    async def get_all(self, model: Type[Base]) -> Optional[List[Any]]:
        """
        Get all instances of a model from the database.
        """
        async with self.Session() as session:
            result = await session.execute(select(model))  # Use `select(model)` for querying
            return result.scalars().all()

    async def get_by(self, model: Type[Base], params: Dict[str, Any]) -> Optional[List[Any]]:
        """
        Get instances of a model by specific parameters.
        """
        async with self.Session() as session:
            query = select(model).filter_by(**params)  # Corrected to use select with filters
            result = await session.execute(query)
            return result.scalars().all()

    async def delete(self, model: Type[Base], instance: Any) -> None:
        """
        Delete an instance of the model from the database.
        """
        async with self.Session() as session:
            async with session.begin():
                await session.delete(instance)
                await session.commit()

    async def update(self, model: Type[Base], instance: Any) -> None:
        """
        Update an existing instance of the model in the database.
        """
        async with self.Session() as session:
            async with session.begin():
                session.merge(instance)
                await session.commit()
