import requests
import json
from cachetools import TTLCache
from helpers.priceConverter import *
from exceptions import ExternalAPIError, DataProcessingError, InternalServerError
from fuzzywuzzy import process

cache = TTLCache(maxsize=100, ttl=300) # Cache for 5 minutes

def load_known_skin_names(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)  # Já é uma lista de strings
    except Exception as e:
        print(f"Error loading skin names: {e}")
        return []

known_skin_names = load_known_skin_names("market_names.json")

def expand_wear_condition(name: str) -> str:
    wear_map = {
        " ft": " field-tested",
        " mw": " minimal wear",
        " fn": " factory new",
        " bs": " battle-scarred",
        " ww": " well-worn",
        " st": " StatTrak™"
    }

    name_lower = name.lower()
    for short, full in wear_map.items():
        if short in name_lower:
            name_lower = name_lower.replace(short, full)
    return name_lower

def get_steam_data():
    try:
        response = requests.get("https://steamcommunity.com/market/priceoverview/?country=PT&currency=3&appid=730&market_hash_name=Fever%20Case")
        response.raise_for_status()

        if response.status_code == 200:
            return response.json()
        else:
            raise ExternalAPIError("Failed to fetch data from Steam API.")
    except requests.exceptions.RequestException as e:
        raise ExternalAPIError(str(e)) 

def search_by_name(name, start, count, currency, sort_by, order):
    name = expand_wear_condition(name)
    cache_key = f"{name}_{start}_{count}_{currency}"
    if cache_key in cache:
        return cache[cache_key]

    base_url = "https://steamcommunity.com/market/search/render/"
    params = {
        "appid": 730,         
        "query": name,
        "norender": 1,        
        "start": start,
        "count": count,
    }

    if sort_by != "default":
        params["sort_column"] = sort_by
    if order != "default":
        params["sort_dir"] = order

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "results" not in data:
            raise DataProcessingError("No results found or the data is malformed.")

        results = []
        fuzzy_results = []

        for item in data.get("results", []):
            item_name = item.get("name")
            best_match = process.extractOne(item_name, known_skin_names)
            if best_match and best_match[1] >= 80:
                fuzzy_results.append((item, best_match[1]))

        selected_items = (
            [item for item, score in fuzzy_results]
            if fuzzy_results else data.get("results", [])
        )

        for item in selected_items:
            price_cents = item.get("sell_price")

            if currency == 1:
                converted = price_cents / 100 if price_cents else None
                symbol = "$"
                price = f"{symbol}{converted}"
            elif currency == 2:
                converted = convert_to_pound(price_cents, from_currency="USD") if price_cents else None
                symbol = "£"
                price = f"{symbol}{converted}"
            else:
                converted = convert_to_eur(price_cents, from_currency="USD") if price_cents else None
                symbol = "€"
                price = f"{converted}{symbol}"

            results.append({
                "name": item.get("name"),
                "price_text": item.get("sell_price_text"),
                "converted_price": f"{price}" if converted else "Unavailable",
            })

        cache[cache_key] = {
            "success": True,
            "start": data.get("start", 0),
            "count": data.get("pagesize", 0),
            "total": data.get("total_count", 0),
            "sort_by": sort_by if sort_by else "default",
            "order": order if order else "default",
            "results": results
        }

        return cache[cache_key]

    except requests.exceptions.RequestException as e:
        raise ExternalAPIError(str(e)) 
    except ValueError as e:
        raise DataProcessingError("Error processing the data.")
    except Exception as e:
        raise InternalServerError(str(e))

