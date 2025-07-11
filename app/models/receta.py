from sqlalchemy import Column, Integer, String
from app.database import Base

class Receta(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, index=True)
    dia = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)  # Breakfast, Lunch, Dinner
    nombre = Column(String, nullable=False)
    ingredientes = Column(String, nullable=False)
    instrucciones = Column(String, nullable=False)
    imagen_url = Column(String, nullable=False)
