from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from scrapers.steam import *
from scrapers.steamweb import *
from models import SearchData, SearchResponse, ItemResponse
from typing import List, Optional
from exceptions import ExternalAPIError, DataProcessingError, InternalServerError
from routers import auth, favorites

app = FastAPI(
    title="SkinPeek API",
    description="API for searching and tracking CS2 skins",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(favorites.router)

@app.get("/steam-data")
async def steam_data():
    try:
        data = get_steam_data()
        return data
    
    except ExternalAPIError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/search-item", response_model=SearchResponse, tags=["Search"])
async def search_item(name: str = Query(..., description="Name of the CS2 skin", example="Case"),
                      start: int = Query(0, description="Starting index for pagination", example=0),
                      count: int = Query(10, description="Number of items to return", example=10), 
                      currency: int = Query(3, description="Currency code (3 for Euro, 2 for Pound)", example=3),
                      sort_by: Optional[str] = Query(None, description="Sort by criteria (e.g., 'name', 'price')", example="price"),
                      order: Optional[str] = Query(None, description="Order of sorting (asc or desc)", example="asc")):
    try:
        raw = search_by_name(name, start, count, currency, sort_by, order)
        if not raw["success"]:
            raise DataProcessingError("No results found or data was malformed.")
        
        return {
            "success":       raw["success"],
            "total_results": raw["total"],
            "start_number":  raw["start"],
            "count_number":  raw["count"],
            "sort_by":       raw["sort_by"],
            "order":         raw["order"],
            "items": [
                SearchData(
                    name=item["name"],
                    price=item["converted_price"],
                )
                for item in raw["results"]
            ]
        }
    
    except ExternalAPIError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except DataProcessingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InternalServerError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    

@app.get("/item-data", response_model=ItemResponse , tags=["Item Data"])
async def item_data(name: str = Query(..., description="Name of the CS2 skin", example="Fever Case"),
                    currency: int = Query(3, description="Currency code (3 for Euro, 2 for Pound)", example=3)):
    try:
        raw = get_item_info(name, currency)
        if not raw["success"]:
            raise DataProcessingError("No results found or data was malformed.")
        
        return {
            "success":              raw["success"],
            "name":                 raw["name"],
            "price_min":            raw["price_min"],
            "price_max":            raw["price_max"],
            "soldToday":            raw["soldToday"],
            "price_latest_sell":    raw["price_latest_sell"],
            "sold24h":              raw["sold24h"],
            "price_latest_sell24h": raw["price_latest_sell24h"],
            "sold7d":               raw["sold7d"],
            "price_latest_sell7d":  raw["price_latest_sell7d"],
            "sold30d":              raw["sold30d"],
            "price_latest_sell30d": raw["price_latest_sell30d"],
            "rarity":               raw["rarity"],
        }
    
    except ExternalAPIError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except DataProcessingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InternalServerError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
@app.get("/all-items", tags=["Item Data"])
async def all_items():
    try:
        get_all_items()
        return "All items retrieved successfully"
    
    except ExternalAPIError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except DataProcessingError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InternalServerError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
                    
