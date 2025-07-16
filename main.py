from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import DEFAULT_LANGUAGE
from app.models import Base
from app.database import engine

app = FastAPI(
    title="ProtocolR2 Backend",
    description="API para el bot de Telegram y futura PWA",
    version="1.0.0"
)

# Crear las tablas automáticamente en PostgreSQL
Base.metadata.create_all(bind=engine)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción puedes limitar esto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta base
@app.get("/")
def read_root():
    return {"status": "ok", "lang_default": DEFAULT_LANGUAGE}

@app.get("/ping")
def ping():
    return {"status": "ok"}
