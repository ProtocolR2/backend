from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

# Crear motor de conexión
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Función para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 👇 Agregar estas dos líneas al final
from app import models
Base.metadata.create_all(bind=engine)
