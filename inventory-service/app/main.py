from fastapi import FastAPI
from .routes import inventory_routes
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Incluir rutas
app.include_router(inventory_routes.router, prefix="/inventory", tags=["inventory"])

@app.get("/")
def read_root():
    return {"message": "Servicio de Inventario Activo"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
