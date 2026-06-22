from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import get_settings
from app.db.init_db import init_db, seed_sources
from app.db.session import SessionLocal

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="FutureYou decision intelligence and scenario simulation API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
def startup() -> None:
    init_db()
    db = SessionLocal()
    try:
        seed_sources(db)
    finally:
        db.close()
