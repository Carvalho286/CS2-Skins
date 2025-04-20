from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import MONGO_URI

MONGO_URL = MONGO_URI

client = AsyncIOMotorClient(MONGO_URL)
db = client.skinpeek
