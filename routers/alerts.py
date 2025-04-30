from fastapi import APIRouter, Depends, HTTPException, status
from pymongo import MongoClient
from helpers.config import MONGO_URI
from helpers.jwt import verify_access_token
from models import UserResponse
from bson.objectid import ObjectId
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
client = MongoClient(MONGO_URI)
db = client.skinpeek
users = db.users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    payload = verify_access_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
    db_user = users.find_one({"_id": ObjectId(user_id)})

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    user_in_db = UserResponse(
        id=str(db_user["_id"]),
        email=db_user["email"],
        username=db_user["username"],
        favorites=db_user.get("favorites", []),
        alerts=db_user.get("alerts", []),
    )

    return user_in_db

# Get favorites of current user
@router.get("/alerts", response_model=UserResponse)
def get_favorites(current_user: UserResponse = Depends(get_current_user)):
    return current_user

# Add a new favorite
@router.post("/alerts", response_model=UserResponse)
def add_alert(alert: dict, current_user: UserResponse = Depends(get_current_user)):
    skin_name = alert.get("skinName")
    price_value = alert.get("priceValue")

    if not skin_name or price_value is None:
        raise HTTPException(status_code=400, detail="Both 'skinName' and 'priceValue' must be provided.")

    # Check if alert already exists
    existing_alerts = current_user.alerts or []
    for existing in existing_alerts:
        if existing["skinName"] == skin_name:
            raise HTTPException(status_code=400, detail="Alert for this skin already exists.")

    # Push the new alert
    users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$push": {"alerts": {"skinName": skin_name, "priceValue": price_value}}}
    )

    # Return the updated user
    updated_user = users.find_one({"_id": ObjectId(current_user.id)})
    return UserResponse(
        id=str(updated_user["_id"]),
        email=updated_user["email"],
        username=updated_user["username"],
        alerts=updated_user.get("alerts", []),
    )


# Remove a favorite
@router.delete("/alerts", response_model=UserResponse)
def remove_alert(alert: str, current_user: UserResponse = Depends(get_current_user)):
    # Check if the alert with this skinName exists
    existing_alerts = current_user.alerts or []
    if not any(a["skinName"] == alert for a in existing_alerts):
        raise HTTPException(status_code=400, detail="Alert not found.")

    # Remove the alert based on skinName
    users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$pull": {"alerts": {"skinName": alert}}}
    )

    # Return the updated user
    updated_user = users.find_one({"_id": ObjectId(current_user.id)})
    return UserResponse(
        id=str(updated_user["_id"]),
        email=updated_user["email"],
        username=updated_user["username"],
        alerts=updated_user.get("alerts", []),
    )
