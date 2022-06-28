from pydantic import BaseModel, constr


class SpaceBase(BaseModel):
    name: constr(max_length=32)
    is_refrigerated: bool
    max_capacity: int


class SpaceCreate(SpaceBase):
    pass


class SpaceUpdate(SpaceBase):
    pass


class Space(SpaceBase):
    id: int
    name: constr(max_length=32)
    is_refrigerated: bool
    max_capacity: int

    class Config:
        orm_mode = True
