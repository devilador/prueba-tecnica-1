from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import os
import requests

load_dotenv()

INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")

router = APIRouter()

@router.get("/")
async def get_inventory():
    response = requests.get(f"{INVENTORY_SERVICE_URL}/inventory")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching inventory")
    return response.json()

@router.post("/")
async def create_inventory_item(item: dict):
    response = requests.post(f"{INVENTORY_SERVICE_URL}/inventory", json=item)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error creating inventory item")
    return response.json()
