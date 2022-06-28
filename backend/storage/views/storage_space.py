from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from .. import crud
from .. import schemas

router = APIRouter(
    prefix='/storage_spaces',
    tags=['storage_spaces'],
    responses={404: {'description': 'Not found'}},
)


def get_db(request: Request):
    return request.state.db


@router.post('/', response_model=schemas.StorageSpace)
async def create_storage_space(
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


@router.get('/', response_model=List[schemas.StorageSpace])
async def read_storage_spaces(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_storage_spaces(db, skip=skip, limit=limit)


@router.get(
    '/{storage_space_id}/',
    response_model=schemas.StorageSpace,
)
async def read_storage_space_by_id(
    storage_space_id: int,
    db: Session = Depends(get_db),
):
    db_storage_space = crud.get_storage_space_by_id(db, storage_space_id)
    if db_storage_space:
        return db_storage_space
    return Response(status_code=404)


@router.put(
    '/{storage_space_id}/',
    response_model=schemas.StorageSpace,
)
async def update_storage_space(
    storage_space_id: int,
    storage_space: schemas.StorageSpaceUpdate,
    db: Session = Depends(get_db),
):
    current_storage_space = crud.get_storage_space_by_id(db, storage_space_id)
    if (
        storage_space.is_refrigerated != current_storage_space.is_refrigerated
        and
        crud.get_items_in_storage_place(db, storage_space_id)
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                'Storage space refregerating can\'t be updated when items '
                'inside.'
            ),
        )
    return crud.update_storage_space(db, storage_space_id, storage_space)


@router.delete(
    '/{storage_space_id}/',
    response_model=bool,
)
async def delete_storage_place(
    storage_space_id: int,
    db: Session = Depends(get_db),
):
    db_storage_space = crud.get_storage_space_by_id(db, storage_space_id)
    if db_storage_space:
        if crud.get_items_in_storage_place(db, storage_space_id):
            raise HTTPException(
                status_code=400,
                detail='Storage space contains items. It can\'t be deleted.',
            )

        crud.delete_storage_place(db, storage_space_id)
        return Response(status_code=204)
    return Response(status_code=404)


@router.get(
    '/{storage_space_id}/items/',
    response_model=List[schemas.Item],
)
async def read_items_in_storage_place(
    storage_space_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_items_in_storage_place(db, storage_space_id)
