from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: str
    category: str
    price: float
    quantity: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    sold_date: Optional[datetime] = None
    sold_quantity: Optional[int] = None
    sold_price: Optional[float] = None

class Product(ProductBase):
    id: int
    sold_date: Optional[datetime]
    sold_quantity: Optional[int]
    sold_price: Optional[float]

    class Config:
        orm_mode = True
