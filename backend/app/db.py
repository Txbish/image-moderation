from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime, timezone

load_dotenv()
client = None
db = None

async def connect_db():
    global client, db
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    db = client.image_moderation

    # Seed tokens
    admin_token = "admin-seed-token"
    user_token = "user-seed-token"
    now = datetime.now(timezone.utc)

    await db.tokens.update_one(
        {"token": admin_token},
        {"$set": {"token": admin_token, "isAdmin": True, "createdAt": now}},
        upsert=True
    )
    await db.tokens.update_one(
        {"token": user_token},
        {"$set": {"token": user_token, "isAdmin": False, "createdAt": now}},
        upsert=True
    )