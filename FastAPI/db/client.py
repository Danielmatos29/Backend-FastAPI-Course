from pymongo import MongoClient

# db_client = MongoClient().local

db_client = MongoClient(
    "mongodb+srv://test:test@cluster0.036klwz.mongodb.net/?appName=Cluster0").test