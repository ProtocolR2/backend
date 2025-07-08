from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)  # Telegram ID
    first_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    language_code = Column(String, default="es")
    dia_actual = Column(Integer, default=1)
    email = Column(String, nullable=True)
    plan = Column(String, default="free")  # free / pro / demo
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class RecetaR2(Base):
    __tablename__ = "recetas_r2"
    id = Column(Integer, primary_key=True)
    dia = Column(Integer)
    comida = Column(Enum("desayuno", "almuerzo", "cena", name="tipo_comida"))
    nombre = Column(String)
    ingredientes = Column(Text)
    preparacion = Column(Text)
    foto_url = Column(String)

class ProgresoUsuario(Base):
    __tablename__ = "progreso_usuarios"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"))
    peso = Column(Float)
    energia = Column(Integer)
    sueno = Column(Integer)
    comentarios = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow)
