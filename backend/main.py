import sys

from fastapi import FastAPI, Request, Response

from settings.base import SessionLocal
from storage.routers import item
from storage.routers import item_type
from storage.routers import storage_space

sys.path.append('..')

# Use existing db
# Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(storage_space.router)
app.include_router(item_type.router)
app.include_router(item.router)


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
