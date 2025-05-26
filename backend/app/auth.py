from fastapi import APIRouter, HTTPException, Header, Depends
from app.db import get_db
import uuid
from datetime import datetime
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId



router = APIRouter()

def serialize_token(token):
    token["_id"] = str(token["_id"])
    return token

class TokenCreateRequest(BaseModel):
    is_admin: bool = False

def check_db(db):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

async def get_admin_token(authorization: str = Header(...),db: AsyncIOMotorDatabase = Depends(get_db)):
    check_db(db)
    token = authorization.replace("Bearer ", "")
    token_doc = await db.tokens.find_one({"token": token, "isAdmin": True})
    if not token_doc:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return token

@router.post("/tokens")
async def create_token(
    req: TokenCreateRequest,
    admin_token: str = Depends(get_admin_token),db: AsyncIOMotorDatabase = Depends(get_db)
):
    check_db(db)
    token = str(uuid.uuid4())
    await db.tokens.insert_one({
        "token": token,
        "isAdmin": req.is_admin,
        "createdAt": datetime.now(datetime.timezone.utc)
    })
    return [serialize_token(token)]

@router.get("/tokens")
async def list_tokens(admin_token: str = Depends(get_admin_token),db: AsyncIOMotorDatabase = Depends(get_db)):
    check_db(db)
    tokens = await db.tokens.find().to_list(100)
    return [serialize_token(token) for token in tokens]

@router.delete("/tokens/{token}")
async def delete_token(token: str, admin_token: str = Depends(get_admin_token),db: AsyncIOMotorDatabase = Depends(get_db)):
    check_db(db)
    result = await db.tokens.delete_one({"token": token})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"deleted": True}
