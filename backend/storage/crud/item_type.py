from sqlalchemy.orm import Session

from .. import models, schemas

def get_item_type_by_id(db: Session, item_type_id: int):
    return db.query(models.ItemType).filter(
        models.ItemType.id == item_type_id
    ).first()

def get_item_type_by_name(db: Session, item_type_name: str):
    return db.query(models.ItemType).filter(
        models.ItemType.name == item_type_name
    ).first()

def get_item_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ItemType).offset(skip).limit(limit).all()

def create_item_type(db: Session, item_type: schemas.ItemType):
    db_item_type = models.ItemType(
        name=item_type.name,
        is_kept_cold=item_type.is_kept_cold,
    )
    db.add(db_item_type)
    db.commit()
    db.refresh(db_item_type)
    return db_item_type


def update_item_type(
    db: Session,
    item_type_id: int,
    item_type: schemas.ItemTypeCreate
):
    db.query(models.ItemType).filter(
        models.ItemType.id == item_type_id
    ).update(item_type.dict())
    db.commit()
    return get_item_type_by_id(db, item_type_id)


def get_items_with_specific_item_type(db: Session, item_type_id: int):
    return db.query(models.Item).filter(
        models.Item.item_type_id == item_type_id
    ).all()


def remove_item_type(db: Session, item_type_id: int):
    db.query(models.ItemType).filter(
        models.ItemType.id == item_type_id
    ).delete()
    db.commit()
    return True
