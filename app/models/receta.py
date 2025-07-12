from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Receta(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, index=True)
    dia = Column(Integer, nullable=False)
    tipo_comida = Column(String, nullable=False)  # Breakfast, Lunch, Dinner
    idioma = Column(String, default="es")  # 'es' o 'en'
    titulo = Column(String, nullable=False)
    descripcion = Column(Text)
    ingredientes = Column(Text)
    instrucciones = Column(Text)
    imagen_url = Column(Text)  # opcional
