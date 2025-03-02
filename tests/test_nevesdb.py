import unittest
import asyncio
from unittest.mock import AsyncMock, patch
from nevesdb import NevesDB, Model


class MockUser(Model):
    """Mock User model for testing."""
    id: int = 1
    name: str = "John Doe"
    password: str = "password"

    def __init__(self, id=None, name=None, password=None, **kwargs):
        super().__init__(**kwargs)
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if password is not None:
            self.password = password


class TestNevesDB(unittest.TestCase):
    """Unit tests for EasyDB functionality."""

    def setUp(self):
        """Set up the EasyDB instance with a mock adapter."""
        self.db = NevesDB(db_type="mysql", db_user="root", db_password="password", db_name="test_db", db_url="localhost:3306")
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Mock database methods
        self.db.add = AsyncMock(return_value={"id": 1, "name": "Alice", "password": "password"})
        self.db.get = AsyncMock(return_value=[{"id": 1, "name": "Alice", "password": "password"}])

    def tearDown(self):
        """Close the event loop after tests."""
        self.loop.close()

    def test_register_models(self):
        """Test if models are registered correctly."""
        with patch.object(self.db.db, "create_table", return_value=None) as mock_create_table:
            self.db.register_models([MockUser])
            mock_create_table.assert_called_once_with(MockUser)

    def test_add_user(self):
        """Test adding a user."""
        user = MockUser(id=1, name="Alice")
        result = self.loop.run_until_complete(self.db.add(user))
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Alice")
        self.assertEqual(result["password"], "password")  # Should return default password

    def test_get_user(self):
        """Test retrieving a user."""
        users = self.loop.run_until_complete(self.db.get(MockUser, {"id": 1}))
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["id"], 1)
        self.assertEqual(users[0]["name"], "Alice")
        self.assertEqual(users[0]["password"], "password")


if __name__ == "__main__":
    unittest.main()