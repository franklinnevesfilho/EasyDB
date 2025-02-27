from .sql_db import SQLDatabase
from .mongo_db import MongoDatabase

adapters = {
    "sqlite": SQLDatabase,
    "postgresql": SQLDatabase,
    "mysql": SQLDatabase,
    "mongodb": MongoDatabase,
}