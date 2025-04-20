import json

with open("config.json") as f:
    config = json.load(f)

STEAMWEBAPI_KEY = config["steamwebapikey"]
MONGO_URI = config["mongouri"]
SECRET_KEY = config["secret_key"] 
ALGORITHM = "HS256"
