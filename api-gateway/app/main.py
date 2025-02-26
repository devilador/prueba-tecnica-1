from fastapi import FastAPI
from .routes import product_routes, user_routes, inventory_routes
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Incluir rutas
app.include_router(product_routes.router, prefix="/products", tags=["products"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(inventory_routes.router, prefix="/inventory", tags=["inventory"])

@app.get("/")
def read_root():
    return {"message": "API Gateway Activo"}


import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
