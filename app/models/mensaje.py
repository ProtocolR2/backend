from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Mensaje(Base):
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, index=True)
    hora = Column(String, nullable=False)  # ej: "07:00"
    tipo = Column(String, default="recordatorio")  # tip, motivacional, etc.
    idioma = Column(String, default="es")
    contenido = Column(Text, nullable=False)
