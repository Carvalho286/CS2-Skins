from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import MONGO_URI
from pymongo import MongoClient

MONGO_URL = MONGO_URI

client = AsyncIOMotorClient(MONGO_URL)
db = client.skinpeek

def get_db():
    client = MongoClient("mongodb://localhost:27017/")  
    db = client["skinpeek"]  
    return db.users 
