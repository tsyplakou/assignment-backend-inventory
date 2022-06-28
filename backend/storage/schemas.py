from pydantic import BaseModel, constr, Field
from datetime import date


class StorageSpaceBase(BaseModel):
    name: str = Field(max_length=32)
    is_refrigerated: bool
    max_capacity: int


class StorageSpaceCreate(StorageSpaceBase):
    pass


class StorageSpaceUpdate(StorageSpaceBase):
    name: str = Field(max_length=32)
    is_refrigerated: bool


class StorageSpace(StorageSpaceBase):
    id: int
    name: str = Field(max_length=32)
    is_refrigerated: bool
    max_capacity: int

    class Config:
        orm_mode = True


class ItemTypeBase(BaseModel):
    name: str = Field(max_length=32)
    is_kept_cold: bool


class ItemTypeCreate(ItemTypeBase):
    pass


class ItemTypeUpdate(ItemTypeBase):
    name: str = Field(max_length=32)


class ItemType(ItemTypeBase):
    id: int
    name: str = Field(max_length=32)
    is_kept_cold: bool

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    name: str = Field(max_length=32)
    expiration_date: date
    item_type_id: int
    storage_space_id: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    name: str = Field(max_length=32)
    storage_space_id: int


class Item(ItemBase):
    id: int
    name: str = Field(max_length=32)
    expiration_date: date
    item_type_id: int
    storage_space_id: int

    class Config:
        orm_mode = True
