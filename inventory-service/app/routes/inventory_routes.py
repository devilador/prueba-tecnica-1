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
async def get_inventory(db: Session = Depends(get_db)):
    inventory = crud.get_inventory(db)
    return inventory

@router.post("/")
async def create_inventory_item(item: schemas.InventoryCreate, db: Session = Depends(get_db)):
    db_item = crud.create_inventory_item(db=db, item=item)
    return db_item
