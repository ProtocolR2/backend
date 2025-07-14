from sqlalchemy import Column, Integer, String
from app.db import Base

class Receta(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, index=True)
    dia = Column(Integer, nullable=False)  # Día 1, Día 2, etc.
    hora = Column(String, nullable=False)  # Ej: "07:00"
    instancia = Column(String, nullable=False)  # Ej: "Desayuno", "Cena"
    titulo = Column(String, nullable=False)  # Nombre del plato
    imagen_url = Column(String, nullable=True)  # Puede estar vacío
    idioma = Column(String, default="es")  # Por defecto español
