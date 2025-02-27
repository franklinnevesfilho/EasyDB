from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from easydb.core import Adapter, logger

Base = declarative_base()


def _build_where_clause(filters: dict):
    """Build the WHERE clause for SQL queries."""
    return " AND ".join([f"{key} = '{value}'" for key, value in filters.items()])


def _build_set_clause(update_data: dict):
    """Build the SET clause for SQL queries."""
    return ", ".join([f"{key} = '{value}'" for key, value in update_data.items()])


def _map_type(py_type):
    """Map Python types to SQLAlchemy column types."""
    if py_type == int:
        return Integer
    elif py_type == str:
        # Default to VARCHAR(255) for string columns to avoid the MySQL error
        return String(255)
    elif py_type == float:
        return Float
    else:
        message = f"Unsupported type: {py_type}"
        logger.error(message)
        raise ValueError(message)


class SQLDatabase(Adapter):

    def __init__(self, db_url: str):
        """Initialize the SQL database connection."""
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_table(self, model_class: type):
        """Create the table based on the model class."""
        columns = []

        # Dynamically create columns based on the model class annotations
        for name, type_ in model_class.__annotations__.items():
            if name == "id" and "id" not in model_class.__dict__:
                # If 'id' is not defined, add it as the primary key
                columns.append(Column(name, Integer, primary_key=True))
            else:
                # For other fields, map to SQLAlchemy types
                columns.append(Column(name, _map_type(type_)))

        # If 'id' wasn't added manually, we can safely add it as a primary key
        if "id" not in model_class.__annotations__ and "id" not in model_class.__dict__:
            columns.append(Column('id', Integer, primary_key=True))

        # Create the SQLAlchemy table
        table = Table(model_class.__name__.lower(), self.metadata, *columns)
        self.metadata.create_all(self.engine)  # Create the table in the DB
        logger.info(f"Table `{model_class.__name__.lower()}` created successfully.")

    async def create(self, table: str, data: dict):
        """Insert a record into the table."""
        query = f"INSERT INTO {table} ({', '.join(data.keys())}) VALUES ({', '.join([':' + k for k in data.keys()])})"
        with self.SessionLocal() as session:
            session.execute(text(query), data)
            session.commit()

    async def get(self, table: str, filters: dict):
        """Read records from the table based on filters."""
        query = f"SELECT * FROM {table} WHERE {_build_where_clause(filters)}"
        with self.SessionLocal() as session:
            result = session.execute(text(query))
            return result.fetchall()

    async def update(self, table: str, filters: dict, update_data: dict):
        """Update records in the table."""
        query = f"UPDATE {table} SET {_build_set_clause(update_data)} WHERE {_build_where_clause(filters)}"
        with self.SessionLocal() as session:
            session.execute(text(query))
            session.commit()

    async def delete(self, table: str, filters: dict):
        """Delete records from the table based on filters."""
        query = f"DELETE FROM {table} WHERE {_build_where_clause(filters)}"
        with self.SessionLocal() as session:
            session.execute(text(query))
            session.commit()


