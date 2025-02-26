from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import os
import requests

load_dotenv()

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL")

router = APIRouter()

@router.get("/")
async def get_products():
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching products")
    return response.json()

@router.post("/")
async def create_product(product: dict):
    response = requests.post(f"{PRODUCT_SERVICE_URL}/products", json=product)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error creating product")
    return response.json()
