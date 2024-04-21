from pymongo.mongo_client import MongoClient

uri = "mongodb://localhost:27017"
client = MongoClient(uri)

db = client["todo_db"]
collection = db["todo_data"]