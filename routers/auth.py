from fastapi import APIRouter, Depends, HTTPException, status
from models import UserIn, UserOut, UserLogin, UserResponse
from helpers.hash import hash_password, verify_password
from pymongo import MongoClient
from bson.objectid import ObjectId
from helpers.config import MONGO_URI
from helpers.jwt import create_access_token, verify_access_token
from datetime import timedelta
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

@router.post("/register", response_model=UserOut)
def register(user: UserIn):
    if users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user.password)
    new_user = {
        "email": user.email,
        "username": user.username,
        "password": hashed_pw,
        "favorites": user.favorites,
        "alerts": user.alerts,
    }
    result = users.insert_one(new_user)
    return {"id": str(result.inserted_id), "email": user.email}

@router.post("/login")
def login(user: UserLogin):
    db_user = users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": str(db_user["_id"])})
    return {"message": "Login successful", "access_token": access_token}
