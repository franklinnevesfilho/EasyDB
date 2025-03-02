from typing import Dict, List, Optional, Type, TypeVar, Any

from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .adapter import Adapter
from ..logger import logger

Base = declarative_base()

T = TypeVar('T', bound='Base')

def _map_type(py_type: Type[int | str | float]) -> Any:
    """Map Python types to SQLAlchemy column types."""
    type_mapping = {
        int: Integer,
        str: String(255),
        float: Float,
    }
    if py_type in type_mapping:
        return type_mapping[py_type]
    else:
        message = f"Unsupported type: {py_type}"
        logger.error(message)
        raise ValueError(message)

class SQLDatabase(Adapter):

    def __init__(self, db_url: str):
        """Initialize the SQL database connection."""
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)

    def create_table(self, model_class: Type[T]):
        """Create the table based on the model class."""
        columns = []

        # Dynamically create columns based on the model class annotations
        for name, type_ in model_class.__annotations__.items():
            if name == "id":
                columns.append(Column(name, Integer, primary_key=True))
            else:
                columns.append(Column(name, _map_type(type_)))

        if "id" not in model_class.__annotations__ and "id" not in model_class.__dict__:
            columns.append(Column('id', Integer, primary_key=True))

        table = Table(model_class.__name__.lower(), self.metadata, *columns)
        self.metadata.create_all(self.engine)
        logger.info(f"Table `{model_class.__name__.lower()}` created successfully.")

    async def add(self, table: str, data: Dict[str, Any]):
        """Insert a record into the table."""
        query = text(f"INSERT INTO {table} ({', '.join(data.keys())}) VALUES ({', '.join([':' + k for k in data.keys()])})")
        try:
            with self.SessionLocal() as session:
                session.execute(query, data)
                session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error creating record in table {table}: {e}")
            raise

    async def get(self, table: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Read records from the table. If filters are provided, apply them; otherwise, return all records."""
        # Build the base query
        query = f"SELECT * FROM {table}"

        # Add WHERE clause if filters are provided
        if filters:
            where_clause = " AND ".join([f"{key} = :{key}" for key in filters.keys()])
            query += f" WHERE {where_clause}"

        # Convert the query to a SQLAlchemy text object
        query = text(query)

        try:
            with self.SessionLocal() as session:
                # Execute the query with filters (if any)
                result = session.execute(query, filters or {})
                # Return all rows as a list of dictionaries
                return [dict(row) for row in result.fetchall()]
        except SQLAlchemyError as e:
            logger.error(f"Error fetching records from table {table}: {e}")
            raise

    async def update(self, table: str, filters: Dict[str, Any], update_data: Dict[str, Any]):
        """Update records in the table."""
        set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        where_clause = " AND ".join([f"{key} = :{key}" for key in filters.keys()])
        query = text(f"UPDATE {table} SET {set_clause} WHERE {where_clause}")
        try:
            with self.SessionLocal() as session:
                session.execute(query, {**update_data, **filters})
                session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error updating records in table {table}: {e}")
            raise

    async def delete(self, table: str, filters: Dict[str, Any]):
        """Delete records from the table based on filters."""
        where_clause = " AND ".join([f"{key} = :{key}" for key in filters.keys()])
        query = text(f"DELETE FROM {table} WHERE {where_clause}")
        try:
            with self.SessionLocal() as session:
                session.execute(query, filters)
                session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error deleting records from table {table}: {e}")
            raise

    async def execute(self, query: str):
        """Execute a raw SQL query."""
        try:
            with self.SessionLocal() as session:
                result = session.execute(text(query))
                session.commit()
                return result
        except SQLAlchemyError as e:
            logger.error(f"Error executing query: {e}")
            raise