from pydantic import BaseModel
from typing import List

class SearchData(BaseModel):
    name: str
    price: str
    price_eur: str

class SearchResponse(BaseModel):
    total_results: int
    items: List[SearchData]
