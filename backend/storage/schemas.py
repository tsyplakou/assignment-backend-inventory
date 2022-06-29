from datetime import date

from pydantic import BaseModel, Field, FutureDate


# class StorageSpaceBase(BaseModel):
#     name: str = Field(max_length=32)
#     is_refrigerated: bool
#     max_capacity: int


class StorageSpaceCreate(BaseModel):
    name: str = Field(max_length=32)
    is_refrigerated: bool
    max_capacity: int


class StorageSpaceUpdate(BaseModel):
    name: str = Field(max_length=32)
    is_refrigerated: bool


class StorageSpace(BaseModel):
    id: int
    name: str = Field(max_length=32)
    is_refrigerated: bool
    max_capacity: int

    class Config:
        orm_mode = True



class ItemTypeCreate(BaseModel):
    name: str = Field(max_length=32)
    is_kept_cold: bool


class ItemTypeUpdate(BaseModel):
    name: str = Field(max_length=32)


class ItemType(BaseModel):
    id: int
    name: str = Field(max_length=32)
    is_kept_cold: bool

    class Config:
        orm_mode = True


class ItemCreate(BaseModel):
    name: str = Field(max_length=32)
    expiration_date: FutureDate
    item_type_id: int
    storage_space_id: int


class ItemUpdate(BaseModel):
    name: str = Field(max_length=32)
    storage_space_id: int


class Item(BaseModel):
    id: int
    name: str = Field(max_length=32)
    expiration_date: date
    item_type_id: int
    storage_space_id: int

    class Config:
        orm_mode = True
