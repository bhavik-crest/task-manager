import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from app.routers import tasks
from app.models import Base
from app.database import engine

app = FastAPI(title="Task Manager API")

logger = logging.getLogger("uvicorn.error")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Be cautious with "*" in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event for DB table creation
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Validation error handler to return friendly error messages
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    friendly_errors = []
    for err in errors:
        loc = " -> ".join(str(loc) for loc in err['loc'] if loc != 'body')
        msg = err['msg']
        friendly_errors.append(f"Error in {loc}: {msg}")
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({
            "detail": friendly_errors,
            "message": "Validation error occurred"
        }),
    )

# Global exception handler for unexpected errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

app.include_router(tasks.router)