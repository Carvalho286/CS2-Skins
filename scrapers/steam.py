import requests
from helpers.priceConverter import *

def get_steam_data():
    response = requests.get("https://steamcommunity.com/market/priceoverview/?country=PT&currency=3&appid=730&market_hash_name=Fever%20Case")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
    
def search_by_name(name):
    base_url = "https://steamcommunity.com/market/search/render/"
    params = {
        "appid": 730,         
        "query": name,
        "norender": 1,        
        "start": 0,
        "count": 10,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("results", []):
            price_cents = item.get("sell_price")
            price_eur = convert_to_eur(price_cents, from_currency="USD") if price_cents else None
            results.append({
                "name": item.get("name"),
                "price_text": item.get("sell_price_text"),
                "price_eur": f"€{price_eur}" if price_eur else "Unavailable",
            })

        return {
            "success": True,
            "total": data.get("total_count", 0),
            "results": results
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
