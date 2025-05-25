from fastapi import APIRouter, HTTPException, Header, Depends
from app.db import db
import uuid
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class TokenCreateRequest(BaseModel):
    is_admin: bool = False

async def get_admin_token(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    token_doc = await db.tokens.find_one({"token": token, "isAdmin": True})
    if not token_doc:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return token

@router.post("/tokens")
async def create_token(
    req: TokenCreateRequest,
    admin_token: str = Depends(get_admin_token)
):
    token = str(uuid.uuid4())
    await db.tokens.insert_one({
        "token": token,
        "isAdmin": req.is_admin,
        "createdAt": datetime.now(datetime.timezone.utc)
    })
    return {"token": token}

@router.get("/tokens")
async def list_tokens(admin_token: str = Depends(get_admin_token)):
    tokens = await db.tokens.find().to_list(100)
    return tokens

@router.delete("/tokens/{token}")
async def delete_token(token: str, admin_token: str = Depends(get_admin_token)):
    result = await db.tokens.delete_one({"token": token})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Token not found")
    return {"deleted": True}
