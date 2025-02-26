from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import os
import requests

load_dotenv()

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")

router = APIRouter()

@router.get("/")
async def get_users():
    response = requests.get(f"{USER_SERVICE_URL}/users")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching users")
    return response.json()

@router.post("/")
async def create_user(user: dict):
    response = requests.post(f"{USER_SERVICE_URL}/users", json=user)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error creating user")
    return response.json()
