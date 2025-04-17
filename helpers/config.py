import json

with open("config.json") as f:
    config = json.load(f)

STEAMWEBAPI_KEY = config["steamwebapikey"]
