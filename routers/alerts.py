from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models import UserInDB, Alert, UserResponse
from database import get_db
from bson import ObjectId
from fastapi import HTTPException
from pymongo.collection import Collection

router = APIRouter()

def get_current_user(db: Collection, user_id: str):
    user = db.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/alerts/", response_model=UserResponse)
async def create_alert(user_id: str, alert: Alert, db: Collection = Depends(get_db)):
    user = get_current_user(db, user_id)
    
    for existing_alert in user.get("alerts", []):
        if existing_alert["skin_name"] == alert.skin_name and existing_alert["currency"] == alert.currency:
            raise HTTPException(status_code=400, detail="Alert for this skin already exists")
    
    db.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"alerts": alert.dict()}}
    )
    updated_user = db.find_one({"_id": ObjectId(user_id)})
    return UserResponse(**updated_user)

@router.get("/alerts/{user_id}", response_model=UserResponse)
async def get_alerts(user_id: str, db: Collection = Depends(get_db)):
    user = get_current_user(db, user_id)
    return UserResponse(**user)

@router.delete("/alerts/{user_id}/{alert_id}", response_model=UserResponse)
async def remove_alert(user_id: str, alert_id: str, db: Collection = Depends(get_db)):
    user = get_current_user(db, user_id)
    
    db.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"alerts": {"_id": ObjectId(alert_id)}}}
    )
    
    updated_user = db.find_one({"_id": ObjectId(user_id)})
    return UserResponse(**updated_user)
