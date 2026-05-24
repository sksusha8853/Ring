from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from config import MONGODB_URL, DATABASE_NAME
import logging

logger = logging.getLogger(__name__)

client = None
db = None

def connect_to_mongo():
    global client, db
    try:
        client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db = client[DATABASE_NAME]
        
        # Create indexes
        users_collection = db['users']
        users_collection.create_index("username", unique=True)
        # Remove email unique index as email is not part of the user signup model
        # If needed in future, make it sparse: users_collection.create_index("email", unique=True, sparse=True)
        try:
            users_collection.drop_index("email_1")
        except:
            pass  # Index might not exist
        
        visits_collection = db['visits']
        visits_collection.create_index("username")
        visits_collection.create_index("timestamp")
        
        logger.info("Connected to MongoDB successfully")
        return db
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

def close_mongo_connection():
    global client
    if client:
        client.close()
        logger.info("Closed MongoDB connection")

def get_database():
    if db is None:
        raise RuntimeError("Database not connected. Call connect_to_mongo() first")
    return db
