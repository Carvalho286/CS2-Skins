from pydantic import BaseModel
from typing import List

class SearchData(BaseModel):
    name: str
    price: str

class SearchResponse(BaseModel):
    total_results: int
    start_number: int
    count_number: int
    sort_by: str
    order: str
    items: List[SearchData]

class ItemResponse(BaseModel):
    success: bool
    name: str
    price_min: str
    price_max: str
    soldToday: int
    price_latest_sell: str
    sold24h: int
    price_latest_sell24h: str
    sold7d: int
    price_latest_sell7d: str
    sold30d: int
    price_latest_sell30d: str
    rarity: str
