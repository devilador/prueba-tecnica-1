from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..database import SessionLocal, engine
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def get_products(db: Session = Depends(get_db)):
    products = crud.get_products(db)
    return products

@router.post("/")
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.create_product(db=db, product=product)
    return db_product
