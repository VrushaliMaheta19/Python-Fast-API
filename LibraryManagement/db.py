import pymongo

MONGODB_URL = "mongodb://localhost:27017"

client = pymongo.MongoClient(MONGODB_URL)

db = client["library"]