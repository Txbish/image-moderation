from fastapi import Request
from app.db import db
from datetime import datetime

async def log_usage(request: Request, call_next):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    response = await call_next(request)
    if token:
        await db.usages.insert_one({
            "token": token,
            "endpoint": request.url.path,
            "timestamp": datetime.now(datetime.timezone.utc)
        })
    return response
