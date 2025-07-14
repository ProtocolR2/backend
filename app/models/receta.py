from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Receta(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, index=True)
    dia = Column(Integer, nullable=False)                      # Día del programa
    tipo_comida = Column(String, nullable=False)               # Ej: "desayuno", "almuerzo", etc.
    idioma = Column(String, default="es")                      # "es", "en", etc.
    titulo = Column(String, nullable=False)                    # Título de la receta
    descripcion = Column(Text, nullable=True)                  # Descripción breve
    ingredientes = Column(Text, nullable=True)                 # Ingredientes detallados
    instrucciones = Column(Text, nullable=True)                # Pasos para preparar
    imagen_url = Column(String, nullable=True)                 # URL en Cloudinary o similar
