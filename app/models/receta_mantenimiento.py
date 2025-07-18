from sqlalchemy import Column, Integer, String
from app.database import Base

class RecetaMantenimiento(Base):
    __tablename__ = "recetas_mantenimiento"

    id = Column(Integer, primary_key=True, index=True)
    dia = Column(Integer, nullable=False)          # Día 1‑365
    hora = Column(String, nullable=False)          # “7:00”, “13:00”, etc.
    instancia = Column(String, nullable=False)     # Desayuno, Almuerzo…
    titulo = Column(String, nullable=False)        # Nombre del plato
    imagen_url = Column(String)                    # URL Cloudinary (puede quedar vacío)
    idioma = Column(String, default="es")          # Idioma (por si luego agregás EN, BR…)
