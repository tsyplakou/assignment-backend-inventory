from sqlalchemy.orm import Session

from . import models, schemas


def get_storage_space_by_id(db: Session, storage_space_id: int):
    return db.query(models.StorageSpace).filter(
        models.StorageSpace.id == storage_space_id
    ).first()

def get_storage_space_by_name(db: Session, storage_space_name: int):
    return db.query(models.StorageSpace).filter(
        models.StorageSpace.name == storage_space_name
    ).first()

def get_storage_spaces(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.StorageSpace).offset(skip).limit(limit).all()

def create_storage_space(db: Session, storage_space: schemas.StorageSpaceCreate):
    db_storage_space = models.StorageSpace(
        name=storage_space.name,
        is_refrigerated=storage_space.is_refrigerated,
        max_capacity=storage_space.max_capacity,
    )
    db.add(db_storage_space)
    db.commit()
    db.refresh(db_storage_space)
    return db_storage_space


def update_storage_space(
    db: Session,
    storage_space_id: int,
    storage_space: schemas.StorageSpaceCreate
):
    db.query(models.StorageSpace).filter(
        models.StorageSpace.id == storage_space_id
    ).update(storage_space.dict())
    db.commit()
    return get_storage_space_by_id(db, storage_space_id)


def get_items_in_storage_place(db: Session, storage_space_id: int):
    return db.query(models.Item).filter(
        models.Item.storage_space_id == storage_space_id
    ).all()


def remove_storage_place(db: Session, storage_space_id: int):
    db.query(models.StorageSpace).filter(
        models.StorageSpace.id == storage_space_id
    ).delete()
    db.commit()
    return True
