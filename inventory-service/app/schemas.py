from pydantic import BaseModel

class InventoryBase(BaseModel):
    name: str
    quantity: int
    price: float

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int

    class Config:
        orm_mode = True
