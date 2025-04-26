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
    )

    return user_in_db

# Get favorites of current user
@router.get("/favorites", response_model=UserResponse)
def get_favorites(current_user: UserResponse = Depends(get_current_user)):
    return current_user

# Add a new favorite
@router.post("/favorites", response_model=UserResponse)
def add_favorite(favorite: str, current_user: UserResponse = Depends(get_current_user)):
    if favorite in current_user.favorites:
        raise HTTPException(status_code=400, detail="Favorite already exists.")
    
    # Update the favorites in the database
    users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$push": {"favorites": favorite}}  # Add to the favorites list
    )
    
    # Return the updated user
    updated_user = users.find_one({"_id": ObjectId(current_user.id)})
    return UserResponse(
        id=str(updated_user["_id"]),
        email=updated_user["email"],
        username=updated_user["username"],
        favorites=updated_user.get("favorites", []),
    )

# Remove a favorite
@router.delete("/favorites", response_model=UserResponse)
def remove_favorite(favorite: str, current_user: UserResponse = Depends(get_current_user)):
    if favorite not in current_user.favorites:
        raise HTTPException(status_code=400, detail="Favorite not found.")
    
    # Update the favorites in the database
    users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$pull": {"favorites": favorite}}  # Remove from the favorites list
    )
    
    # Return the updated user
    updated_user = users.find_one({"_id": ObjectId(current_user.id)})
    return UserResponse(
        id=str(updated_user["_id"]),
        email=updated_user["email"],
        username=updated_user["username"],
        favorites=updated_user.get("favorites", []),
    )
