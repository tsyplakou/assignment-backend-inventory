from sqlalchemy.orm import Session

from . import models, schemas


def get_space(db: Session, space_id: int):
    return db.query(models.Space).filter(models.Space.id == space_id).first()

def get_space_by_name(db: Session, space_name: int):
    return db.query(models.Space).filter(
        models.Space.name == space_name
    ).first()

def get_spaces(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Space).offset(skip).limit(limit).all()

def create_space(db: Session, space: schemas.SpaceCreate):
    db_space = models.Space(
        name=space.name,
        is_refrigerated=space.is_refrigerated,
    )
    db.add(db_space)
    db.commit()
    db.refresh(db_space)
    return db_space
