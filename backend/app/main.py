from fastapi import FastAPI
from app.routers import tasks
from app.models import Base
from app.database import engine
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Task Manager API")

origins = [
    "http://localhost:3000",  # your frontend origin
    "http://127.0.0.1:8000", # sometimes localhost resolves differently
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # or ["*"] to allow all origins (not recommended in production)
    allow_credentials=True,
    allow_methods=["*"],         # allows all methods GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],         # allow all headers like authorization, content-type, etc.
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(tasks.router)
