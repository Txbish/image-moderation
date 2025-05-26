from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.auth import router as auth_router
from app.moderate import router as moderate_router
from app.middleware import log_usage
from app.db import connect_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    db=await connect_db()
    app.state.db = db
    yield

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.middleware("http")(log_usage)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth_router, prefix="/auth")
    app.include_router(moderate_router, prefix="")
    return app

app = create_app()