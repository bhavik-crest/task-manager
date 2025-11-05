from fastapi import FastAPI, Request
from app.routers import tasks
from app.models import Base
from app.database import engine
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    # Transform Pydantic errors into simple, user-friendly messages
    friendly_errors = []
    for err in errors:
        loc = " -> ".join(str(loc) for loc in err['loc'] if loc != 'body')  # exclude 'body' in path
        msg = err['msg']
        friendly_errors.append(f"Error in {loc}: {msg}")
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            "detail": friendly_errors,
            "message": "Validation error occurred"
        }),
    )

app.include_router(tasks.router)
