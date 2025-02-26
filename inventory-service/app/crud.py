from sqlalchemy.orm import Session
from . import models, schemas

def get_inventory(db: Session):
    return db.query(models.InventoryItem).all()

def create_inventory_item(db: Session, item: schemas.InventoryCreate):
    db_item = models.InventoryItem(name=item.name, quantity=item.quantity, price=item.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
