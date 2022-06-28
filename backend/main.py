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


@app.post("/spaces/", response_model=schemas.Space)
def create_space(space: schemas.SpaceCreate, db: Session = Depends(get_db)):
    db_space = crud.get_space_by_name(db, space.name)
    if db_space:
        raise HTTPException(status_code=400, detail="Space with this name already exists.")
    return crud.create_space(db=db, space=space)


@app.get("/spaces/", response_model=List[schemas.Space])
def read_spaces(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    spaces = crud.get_spaces(db, skip=skip, limit=limit)
    return spaces
