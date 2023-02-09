import pymongo
from config import (
    MONGODB_PASSWORD,
    MONGODB_USER
)
from pymongo.collection import Collection

client = pymongo.MongoClient(
    f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASSWORD}@cluster0.2s74d.mongodb.net/?retryWrites=true&w=majority"
)
db = client.test
collection: Collection = db.get_collection("todo")
