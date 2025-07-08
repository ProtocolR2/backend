from fastapi import FastAPI
from app.routes import user
from app.database import Base, engine

app = FastAPI()

# Crear tablas en la DB al iniciar
Base.metadata.create_all(bind=engine)

# Rutas
app.include_router(user.router)
