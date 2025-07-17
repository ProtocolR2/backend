from sqlalchemy import Column, Integer, String
from app.database import Base

class Mensaje(Base):
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, index=True)
    dia = Column(Integer, nullable=False)                 # Nuevo campo: Día del mensaje
    hora = Column(String, nullable=False)                 # Nuevo campo: Hora del mensaje
    contenido = Column(String, nullable=False)            # Contenido del mensaje
    idioma = Column(String, default="es", nullable=False) # Idioma (por defecto 'es')
