from pymongo import MongoClient
from bson import ObjectId
from .adapter import Adapter
from typing import Dict, Any


def create_object_id(obj_id: str) -> ObjectId:
    """Create an ObjectId for MongoDB queries."""
    return ObjectId(obj_id)


class MongoDatabase(Adapter):
    def __init__(self, db_url: str, db_name: str):
        """Initialize the MongoDB database connection."""
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        print(f"Connected to MongoDB at {db_url}, using database {db_name}")

    def create_table(self, collection_name: str):
        """Create a collection in MongoDB."""
        # MongoDB automatically creates collections when they are first used.
        # This is just to confirm the collection creation.
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)
            print(f"Collection `{collection_name}` created successfully.")
        else:
            print(f"Collection `{collection_name}` already exists.")

    async def add(self, collection: str, data: Dict[str, Any]):
        """Insert a record into the collection."""
        collection_obj = self.db[collection]
        result = collection_obj.insert_one(data)
        print(f"Document inserted with _id: {result.inserted_id}")
        return result.inserted_id

    async def get(self, collection: str, filters: Dict[str, Any]):
        """Retrieve records from the collection based on filters."""
        collection_obj = self.db[collection]
        result = collection_obj.find(filters)
        return list(result)

    async def update(self, collection: str, filters: Dict[str, Any], update_data: Dict[str, Any]):
        """Update records in the collection."""
        collection_obj = self.db[collection]
        result = collection_obj.update_many(filters, {"$set": update_data})
        print(f"{result.modified_count} document(s) updated.")
        return result.modified_count

    async def delete(self, collection: str, filters: Dict[str, Any]):
        """Delete records from the collection based on filters."""
        collection_obj = self.db[collection]
        result = collection_obj.delete_many(filters)
        print(f"{result.deleted_count} document(s) deleted.")
        return result.deleted_count

