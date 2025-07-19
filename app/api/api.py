from fastapi import APIRouter
from app.api.routes import setup  # 👈 importar tu archivo setup.py

api_router = APIRouter()

# Incluir el router de setup
api_router.include_router(setup.router)
