from fastapi import FastAPI, Request, Response

from settings.base import SessionLocal
from storage.views import item
from storage.views import item_type
from storage.views import storage_space

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
