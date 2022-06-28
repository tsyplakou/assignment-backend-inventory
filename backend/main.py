from typing import List

from fastapi import Depends, HTTPException
from fastapi import FastAPI, Request, Response
from sqlalchemy.orm import Session

from db import Base, engine, SessionLocal, schemas, crud

# Use existing db
# Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    return request.state.db


@app.post('/storage_spaces/', response_model=schemas.StorageSpace)
def create_storage_space(
    storage_space: schemas.StorageSpaceCreate,
    db: Session = Depends(get_db),
):
    db_storage_space = crud.get_storage_space_by_name(db, storage_space.name)
    if db_storage_space:
        raise HTTPException(
            status_code=400,
            detail='Storage space with this name already exists.',
        )
    return crud.create_storage_space(db=db, storage_space=storage_space)


@app.get('/storage_spaces/', response_model=List[schemas.StorageSpace])
def read_storage_spaces(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_storage_spaces(db, skip=skip, limit=limit)


@app.get(
    '/storage_spaces/{storage_space_id}/',
    response_model=schemas.StorageSpace,
)
def read_storage_space_by_id(
    storage_space_id: int,
    db: Session = Depends(get_db),
):
    db_storage_space = crud.get_storage_space_by_id(db, storage_space_id)
    if db_storage_space:
        return db_storage_space
    return Response(status_code=404)


@app.put(
    '/storage_spaces/{storage_space_id}/',
    response_model=schemas.StorageSpace,
)
def update_storage_space(
    storage_space_id: int,
    storage_space: schemas.StorageSpaceCreate,
    db: Session = Depends(get_db),
):
    # can;t remove refrigarated if items inside
    return crud.update_storage_space(db, storage_space_id, storage_space)


@app.delete(
    '/storage_spaces/{storage_space_id}/',
    response_model=bool,
)
def read_items_in_storage_place(
    storage_space_id: int,
    db: Session = Depends(get_db),
):
    db_storage_space = crud.get_storage_space_by_id(db, storage_space_id)
    if db_storage_space:
        crud.remove_storage_place(db, storage_space_id)
        return Response(status_code=204)
    return Response(status_code=404)


@app.get(
    '/storage_spaces/{storage_space_id}/items/',
    response_model=List[schemas.Item],
)
def read_items_in_storage_place(
    storage_space_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_items_in_storage_place(db, storage_space_id)
