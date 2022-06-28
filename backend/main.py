from typing import List

from fastapi import Depends, HTTPException
from fastapi import FastAPI, Request, Response
from sqlalchemy.orm import Session

from db import Base, engine, SessionLocal, schemas, crud

# Use existing db
# Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    return request.state.db


@app.post("/storage_spaces/", response_model=schemas.StorageSpace)
def create_storage_space(
    storage_space: schemas.StorageSpaceCreate,
    db: Session = Depends(get_db),
):
    db_storage_space = crud.get_storage_space_by_name(db, storage_space.name)
    if db_storage_space:
        raise HTTPException(
            status_code=400,
            detail="Storage space with this name already exists.",
        )
    return crud.create_storage_space(db=db, storage_space=storage_space)


@app.get("/storage_spaces/", response_model=List[schemas.StorageSpace])
def read_storage_spaces(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    storage_spaces = crud.get_storage_spaces(db, skip=skip, limit=limit)
    return storage_spaces
