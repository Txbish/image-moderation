from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.auth import router as auth_router
from app.moderate import router as moderate_router
from app.middleware import log_usage
from app.db import connect_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.middleware("http")(log_usage)
    app.include_router(auth_router, prefix="/auth")
    app.include_router(moderate_router, prefix="")
    return app

app = create_app()