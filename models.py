from pydantic import BaseModel, EmailStr
from typing import List, Optional
from bson import ObjectId

class ObjectIdStr(str):
    """ Custom str subclass to handle Mongo ObjectId conversion to string """
    pass

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

class UserIn(BaseModel):
    email: EmailStr
    username: str
    password: str
    favorites: list[str] = []
    alerts: list[str] = []

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: EmailStr

class UserInDB(BaseModel):
    id: ObjectIdStr
    email: EmailStr
    username: str
    favorites: List[str] = []
    alerts: List[str] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    favorites: List[str]
    alerts: Optional[List[str]] = [] 

    class Config:
        from_attributes = True

class Alert(BaseModel):
    skin_name: str
    price_threshold: float
    currency: str