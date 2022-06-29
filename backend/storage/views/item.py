from typing import List

from fastapi import APIRouter, Depends, Request, Response
from fastapi import HTTPException
from sqlalchemy.orm import Session

from .. import crud
from .. import schemas

router = APIRouter(
    prefix='/items',
    tags=['items'],
    responses={404: {'description': 'Not found'}},
)

def get_db(request: Request):
    return request.state.db


@router.get('/', response_model=List[schemas.Item])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_items(db, skip=skip, limit=limit)


@router.get('/expired/', response_model=List[schemas.Item])
async def read_expired_items(db: Session = Depends(get_db)):
    return crud.get_expired_items(db)


@router.post('/', response_model=schemas.ItemCreate)
async def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
):
    storage = crud.get_storage_space_by_id(db, item.storage_space_id)
    items_in_storage_count = len(
        crud.get_items_in_storage_place(db, item.storage_space_id)
    )
    if items_in_storage_count >= storage.max_capacity:
        raise HTTPException(
            status_code=400,
            detail='Storage space is full.',
        )
    item_type = crud.get_item_type_by_id(db, item.item_type_id)
    if item_type.is_kept_cold and not storage.is_refrigerated:
        raise HTTPException(
            status_code=400,
            detail='This item should be placed to refrigerated storage.',
        )

    return crud.create_item(db=db, item=item)


@router.get(
    '/{item_id}/',
    response_model=schemas.Item,
)
async def read_item_by_id(
    item_id: int,
    db: Session = Depends(get_db),
):
    db_item = crud.get_item_by_id(db, item_id)
    if db_item:
        return db_item
    return Response(status_code=404)


@router.put(
    '/{item_id}/',
    response_model=schemas.Item,
)
async def update_item(
    item_id: int,
    item: schemas.ItemUpdate,
    db: Session = Depends(get_db),
):
    current_item = crud.get_item_by_id(db ,item_id)
    storage = crud.get_storage_space_by_id(db, item.storage_space_id)
    items_in_storage_count = len(
        crud.get_items_in_storage_place(db, item.storage_space_id)
    )
    if (
        current_item.storage_space_id != item.storage_space_id and
        items_in_storage_count >= storage.max_capacity
    ):
        raise HTTPException(
            status_code=400,
            detail='Storage space is full.',
        )
    item_type = crud.get_item_type_by_id(db, current_item.item_type_id)
    if item_type.is_kept_cold and not storage.is_refrigerated:
        raise HTTPException(
            status_code=400,
            detail='This item should be placed to refrigerated storage.',
        )
    return crud.update_item(db, item_id, item)


@router.delete(
    '/{item_id}/',
    response_model=schemas.Item,
)
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    db_item = crud.get_item_by_id(db, item_id)
    if db_item:
        crud.delete_item(db, item_id)
        return Response(status_code=204)
    return Response(status_code=404)
