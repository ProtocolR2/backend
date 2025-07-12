from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Plan(Base):
    __tablename__ = "planes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    duracion_dias = Column(Integer, nullable=False)
    descripcion = Column(Text)
    idioma = Column(String, default="es")
