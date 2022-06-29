from sqlalchemy.orm import Session
from datetime import datetime
from .. import models, schemas

def get_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(
        models.Item.id == item_id
    ).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.Item):
    db_item = models.Item(
        name=item.name,
        expiration_date=item.expiration_date,
        item_type_id=item.item_type_id,
        storage_space_id=item.storage_space_id,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(
    db: Session,
    item_id: int,
    item: schemas.ItemUpdate
):
    db.query(models.Item).filter(
        models.Item.id == item_id
    ).update(item.dict())
    db.commit()
    return get_item_by_id(db, item_id)


def delete_item(db: Session, item_id: int):
    db.query(models.Item).filter(
        models.Item.id == item_id
    ).delete()
    db.commit()
    return True


def get_expired_items(db: Session):
    return db.query(models.Item).filter(
        models.Item.expiration_date <= datetime.now().date()
    ).all()
