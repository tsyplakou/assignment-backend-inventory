from sqlalchemy.orm import Session

from . import models, schemas


def get_storage_space(db: Session, storage_space_id: int):
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
