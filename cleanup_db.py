#!/usr/bin/env python
"""Clean up the MongoDB database - remove problematic indexes and test data"""

from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "qr_contact_app")

print("Connecting to MongoDB...")
client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
db = client[DATABASE_NAME]
users_collection = db['users']

print("Dropping email_1 index...")
try:
    users_collection.drop_index("email_1")
    print("✓ Successfully dropped email_1 index")
except Exception as e:
    print(f"✓ Index doesn't exist or already dropped: {e}")

print("Deleting test users...")
try:
    result = users_collection.delete_many({"username": {"$in": ["skumarsingh3", "testuser123"]}})
    print(f"✓ Deleted {result.deleted_count} test users")
except Exception as e:
    print(f"✗ Error deleting users: {e}")

print("\nDatabase cleanup complete!")
client.close()
