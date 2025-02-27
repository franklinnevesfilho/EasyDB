from nevesdb.core import Adapter


class MockAdapter(Adapter):
    """Mock Adapter to simulate database interactions."""

    def __init__(self):
        self.tables = {}  # Simulate an in-memory storage for tables

    def create_table(self, model: type):
        """Simulate creating a table by storing model structure."""
        table_name = model.__name__.lower()
        self.tables[table_name] = []  # Store data as a list

    async def create(self, table_name, data):
        """Simulate inserting data into a table."""
        if table_name in self.tables:
            self.tables[table_name].append(data)
            return data  # Simulate successful insertion
        return None  # Table doesn't exist

    async def get(self, table_name, query):
        """Simulate querying data from a table."""
        return [row for row in self.tables.get(table_name, []) if all(row[k] == v for k, v in query.items())]

    async def update(self, table_name, query, update):
        """Simulate updating data in a table."""
        updated_count = 0
        for row in self.tables.get(table_name, []):
            if all(row[k] == v for k, v in query.items()):
                row.update(update)
                updated_count += 1
        return {"matched_count": updated_count, "modified_count": updated_count}

    async def delete(self, table_name, query):
        """Simulate deleting data from a table."""
        initial_count = len(self.tables.get(table_name, []))
        self.tables[table_name] = [row for row in self.tables.get(table_name, []) if not all(row[k] == v for k, v in query.items())]
        deleted_count = initial_count - len(self.tables[table_name])
        return {"deleted_count": deleted_count}
