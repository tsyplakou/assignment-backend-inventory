from typing import List
from fastapi import Depends, HTTPException
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from settings.dependencies import get_db
from .. import db_client
from .. import schemas

router = APIRouter(
    prefix='/item_types',
    tags=['item_types'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/', response_model=List[schemas.ItemType])
async def read_item_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return db_client.get_item_types(db, skip=skip, limit=limit)


@router.post('/', response_model=schemas.ItemType)
async def create_item_type(
    item_type: schemas.ItemTypeCreate,
    db: Session = Depends(get_db),
):
    db_item_type = db_client.get_item_type_by_name(db, item_type.name)
    if db_item_type:
        raise HTTPException(
            status_code=400,
            detail='Item type with this name already exists.',
        )
    return db_client.create_item_type(db=db, item_type=item_type)


@router.get(
    '/{item_type_id}/',
    response_model=schemas.ItemType,
)
async def read_item_type_by_id(
    item_type_id: int,
    db: Session = Depends(get_db),
):
    db_item_type = db_client.get_item_type_by_id(db, item_type_id)
    if db_item_type:
        return db_item_type
    return Response(status_code=404)


@router.put(
    '/{item_type_id}/',
    response_model=schemas.ItemType,
)
async def update_item_type(
    item_type_id: int,
    item_type: schemas.ItemTypeUpdate,
    db: Session = Depends(get_db),
):
    current_item_type = db_client.get_item_type_by_id(db, item_type_id)
    if (
        item_type.is_kept_cold != current_item_type.is_kept_cold and
        db_client.get_items_with_specific_item_type(db, item_type_id)
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                'Item type freeze property can\'t be updated when items with '
                'the type exists.'
            ),
        )
    return db_client.update_item_type(db, item_type_id, item_type)


@router.delete(
    '/{item_type_id}/',
    response_model=schemas.ItemType,
)
async def delete_item_type(
    item_type_id: int,
    db: Session = Depends(get_db),
):
    db_item_type = db_client.get_item_type_by_id(db, item_type_id)
    if db_item_type:
        if db_client.get_items_with_specific_item_type(db, item_type_id):
            raise HTTPException(
                status_code=400,
                detail='Items with this type exist. It can\'t be deleted.',
            )

        db_client.delete_item_type(db, item_type_id)
        return Response(status_code=204)
    return Response(status_code=404)
