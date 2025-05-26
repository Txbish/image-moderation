# middleware.py
from fastapi import Request, HTTPException
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)

async def log_usage(request: Request, call_next):
    db: AsyncIOMotorDatabase = request.app.state.db
    
    token = None
    if "authorization" in request.headers:
        try:
            auth_header = request.headers["authorization"]
            token = auth_header.replace("Bearer ", "")
        except Exception as e:
            logger.warning(f"Error parsing auth header: {e}")
    
    timestamp = datetime.now(timezone.utc)
    
    
    if db is not None:
        try:
            await db.usages.insert_one({
                "token": token,
                "endpoint": endpoint,
                "timestamp": timestamp,
            })
        except Exception as e:
            logger.error(f"Failed to log usage: {e}")
    
    response = await call_next(request)
    return response