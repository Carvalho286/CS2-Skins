import requests
import json
from cachetools import TTLCache
from helpers.priceConverter import *
from exceptions import ExternalAPIError, DataProcessingError, InternalServerError
from helpers.config import STEAMWEBAPI_KEY

cache = TTLCache(maxsize=100, ttl=300) # Cache for 5 minutes

def get_item_info(name, currency):
    cache_key = f"{name}_{currency}"
    if cache_key in cache:
        return cache[cache_key]
    
    if currency == 1:
        coin = "USD"
        symbol = "$"
    elif currency == 2:
        coin = "GBP"
        symbol = "£"
    elif currency == 3:
        coin = "EUR"
        symbol = "€"
    else:   
        coin = "EUR"
        symbol = "€"

    base_url = "https://www.steamwebapi.com/steam/api/item"
    params = {
        "key": STEAMWEBAPI_KEY,
        "market_hash_name": name,
        "game": "csgo",
        "currency": coin,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        data = response.json()

        if "id" not in data:
            raise DataProcessingError("No results found or the data is malformed.")
        
        price_min = f"{symbol}{float(data.get('pricemin')):.2f}" if data.get("pricemin") else None
        price_max = f"{symbol}{float(data.get('pricemax')):.2f}" if data.get("pricemax") else None
        price_latest_sell = f"{symbol}{float(data.get('pricelatestsell')):.2f}" if data.get("pricelatestsell") else None
        price_latest_sell24h = f"{symbol}{float(data.get('pricelatestsell24h')):.2f}" if data.get("pricelatestsell24h") else None
        price_latest_sell7d = f"{symbol}{float(data.get('pricelatestsell7d')):.2f}" if data.get("pricelatestsell7d") else None
        price_latest_sell30d = f"{symbol}{float(data.get('pricelatestsell30d')):.2f}" if data.get("pricelatestsell30d") else None


        cache[cache_key] = {
            "success": True,
            "name": data["marketname"],
            "price_min": price_min,
            "price_max": price_max,
            "soldToday": data["soldtoday"],
            "price_latest_sell": price_latest_sell,
            "sold24h": data["sold24h"],
            "price_latest_sell24h": price_latest_sell24h,
            "sold7d": data["sold7d"],
            "price_latest_sell7d": price_latest_sell7d,
            "sold30d": data["sold30d"],
            "price_latest_sell30d": price_latest_sell30d,
            "rarity": data["rarity"],
        }
        
        return cache[cache_key]

    except requests.exceptions.RequestException as e:
        raise ExternalAPIError(str(e))
    except ValueError as e:
        raise DataProcessingError("Error processing the data.")
    except Exception as e:
        raise InternalServerError(str(e)) 
    
def get_all_items():
    base_url = "https://www.steamwebapi.com/steam/api/items"
    params = {
        "key": STEAMWEBAPI_KEY,
        "game": "cs2",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    market_names = [item['marketname'] for item in data]

    with open('market_names.json', 'w') as outfile:
        json.dump(market_names, outfile, indent=4)
        