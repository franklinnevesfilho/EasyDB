from sqlalchemy import Integer, String

from nevesdb import NevesDB, Model, SQLAdapter
import asyncio  # You'll need asyncio to run async functions

# Initialize the database (SQL database in this case)
db = NevesDB(adapter=SQLAdapter, db_user="root", db_password="password", db_name="test_db", db_uri="localhost:3306")


# Define a model with default values
class User(Model):
    id: Integer
    name: String[255]
    password: String[255]


# Register the model (creates the table)
db.register_models([User])

# Create an instance of the User model
user1 = User(id=1, name="Alice")