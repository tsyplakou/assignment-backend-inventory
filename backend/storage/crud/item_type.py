from sqlalchemy.orm import Session

from .. import models, schemas


def get_item_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ItemType).offset(skip).limit(limit).all()
