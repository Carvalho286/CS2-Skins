from fastapi import FastAPI, Query
from scrapers.steam import *
from models import SearchData, SearchResponse
from typing import List

app = FastAPI()

@app.get("/steam-data")
async def steam_data():
    data = get_steam_data()
    return data

@app.get("/search-item", response_model=SearchResponse)
async def search_item(name: str = Query(..., description="Name of the CS2 skin")):
    raw = search_by_name(name)
    if not raw["success"]:
        return {"total_results": 0, "items": []}

    return {
        "total_results": raw["total"],
        "items": [
            SearchData(
                name=item["name"],
                price=item["price_text"],
                price_eur=item["price_eur"],
            )
            for item in raw["results"]
        ]
    }
