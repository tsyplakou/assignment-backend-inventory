from pydantic import BaseModel, constr


class StorageSpaceBase(BaseModel):
    name: constr(max_length=32)
    is_refrigerated: bool
    max_capacity: int


class StorageSpaceCreate(StorageSpaceBase):
    pass


class StorageSpaceUpdate(StorageSpaceBase):
    pass


class StorageSpace(StorageSpaceBase):
    id: int
    name: constr(max_length=32)
    is_refrigerated: bool
    max_capacity: int

    class Config:
        orm_mode = True
