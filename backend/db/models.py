import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .base import Base


class StorageSpace(Base):
    __tablename__ = 'storage_space'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String(32), nullable=False, unique=True)
    is_refrigerated = sa.Column(sa.Boolean, nullable=False)
    max_capacity = sa.Column(sa.Integer, nullable=False)
    items = relationship('Item', back_populates='storage_space')

    def __init__(self, name, is_refrigerated, max_capacity):
        self.name = name
        self.is_refrigerated = is_refrigerated
        self.max_capacity = max_capacity

    def __repr__(self):
        return '<StorageSpace(name="{}", is_refrigerated="{}")>'.format(
            self.name,
            self.is_refrigerated,
        )


class ItemType(Base):
    __tablename__ = 'item_type'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String(32), nullable=False, unique=True)
    is_kept_cold = sa.Column(sa.Boolean, nullable=False)
    items = relationship(
        'Item',
        back_populates='item_type',
        cascade="save-update",
    )

    def __init__(self, name, is_kept_cold):
        self.name = name
        self.is_kept_cold = is_kept_cold

    def __repr__(self):
        return '<ItemType(name="{}", is_kept_cold="{}")>'.format(
            self.name,
            self.is_kept_cold,
        )


class Item(Base):
    __tablename__ = 'item'
    __table_args__ = {'extend_existing': True}

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String(32), nullable=False)
    expiration_date = sa.Column(sa.Date, nullable=False)
    item_type_id = sa.Column(
        ItemType.id.type,
        sa.ForeignKey(ItemType.id),
        nullable=False,
    )
    item_type = relationship(
        'ItemType',
        back_populates='items',
        lazy='joined',
    )
    storage_space_id = sa.Column(
        StorageSpace.id.type,
        sa.ForeignKey(StorageSpace.id),
        nullable=False,
    )
    storage_space = relationship(
        'StorageSpace',
        back_populates='items',
        lazy='joined',
        cascade="save-update",
    )

    def __init__(self, name, expiration_date, item_type_id, storage_space_id):
        self.name = name
        self.is_kept_cold = expiration_date
        self.item_type_id = item_type_id
        self.storage_space_id = storage_space_id

    def __repr__(self):
        return '<Item(name="{}", expiration_date="{}")>'.format(
            self.name,
            self.expiration_date,
        )
