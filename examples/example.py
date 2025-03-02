from nevesdb import NevesDB, Model
import asyncio  # You'll need asyncio to run async functions

# Initialize the database (SQL database in this case)
db = NevesDB(db_type="mysql", db_user="root", db_password="password", db_name="test_db", db_url="localhost:3306")


# Define a model with default values
class User(Model):
    id: int
    name: str
    password: str


# Register the model (creates the table)
db.register_models([User])

# Create an instance of the User model
user1 = User(id=1, name="Alice")


async def add_user(user: User):
    """Add a user to the database."""
    await db.add(user)


async def get_user(user_id: int):
    """Get a user from the database."""
    return await db.get(User, {"id": user_id})


# Run the async functions within an event loop
async def main():
    # Insert the user into the database
    await add_user(user1)

    # Retrieve the user from the database
    users = await get_user(1)

    print(users)  # [{'id': 1, 'name': 'Alice', 'password': 'password'}]


# Execute the main async function
asyncio.run(main())
