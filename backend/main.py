from typing import List

from fastapi import Depends, HTTPException
from fastapi import FastAPI, Request, Response
from sqlalchemy.orm import Session

from settings.base import SessionLocal, engine
from storage import schemas, crud
from storage.models import Base
from storage.views import storage_space

# Use existing db
# Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(storage_space.router)


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
