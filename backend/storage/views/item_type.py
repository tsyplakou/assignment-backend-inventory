from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from .. import crud

router = APIRouter(
    prefix='/item_types',
    tags=['item_types'],
    responses={404: {'description': 'Not found'}},
)

def get_db(request: Request):
    return request.state.db


@router.get('/')
async def read_storage_spaces(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_item_types(db, skip=skip, limit=limit)
