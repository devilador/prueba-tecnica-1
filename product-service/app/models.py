from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    category = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    sold_date = Column(DateTime, nullable=True)
    sold_quantity = Column(Integer, nullable=True)
    sold_price = Column(Float, nullable=True)
