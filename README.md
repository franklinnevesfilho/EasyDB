# EasyData

EasyData is a lightweight, easy-to-use asynchronous database ORM for Python. It simplifies database interactions by providing an intuitive interface for defining models, adding data, and retrieving records.

## Features
- Asynchronous support
- Simple model definition
- Easy database initialization
- Automatic table creation
- Built-in CRUD operations

## Installation

Ensure you have Python installed. Then, install `EasyData` via pip:

```bash
pip install easydata  # Replace with actual package name if different
```

## Usage

### 1. Initialize the Database

Create an instance of `EasyData` and connect to your database:

```python
from easydata import EasyData

# Initialize the database (MySQL example)
db = EasyData(db_type="mysql", db_user="root", db_password="password", db_name="test_db", db_url="localhost:3306")
```

### 2. Define a Model

Models define the structure of your database tables:

```python
from easydata import Model


class User(Model):
    id: int = 1
    name: str = "John Doe"
    password: str = "password"
```

### 3. Register Models

Register the model to create the corresponding table in the database:

```python
db.register_models([User])
```

### 4. Perform CRUD Operations

#### Add a User

```python
import asyncio

async def add_user(user: User):
    await db.add(user)

user1 = User(id=1, name="Alice")
asyncio.run(add_user(user1))
```

#### Retrieve a User

```python
async def get_user(user_id: int):
    return await db.get(User, {"id": user_id})

users = asyncio.run(get_user(1))
print(users)  # [{'id': 1, 'name': 'Alice', 'password': 'password'}]
```

## Running the Example

To run the full example:

```python
async def main():
    await add_user(user1)
    users = await get_user(1)
    print(users)

asyncio.run(main())
```

## License
This project is licensed under the MIT License.

## Contributions
Contributions are welcome! Feel free to open an issue or submit a pull request.

## Contact
For questions, reach out to the repository maintainers or create an issue.

