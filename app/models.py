from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)  # Clave primaria autoincremental
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)  # ID único que usa Telegram para identificar al usuario
    first_name = Column(String, nullable=True)        # Nombre
    username = Column(String, nullable=True)          # Username de Telegram
    language_code = Column(String, default="es")      # Idioma preferido, por defecto español
    dia_actual = Column(Integer, default=1)           # Día actual en el programa (ejemplo: día 1 de 21)
    email = Column(String, nullable=True)             # Email del usuario (opcional)
    plan = Column(String, default="free")             # Plan del usuario (free, pro, demo)
    is_verified = Column(Boolean, default=False)      # Si está verificado o no
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Fecha de creación automática

class RecetaR2(Base):
    __tablename__ = "recetas_r2"
    id = Column(Integer, primary_key=True)
    dia = Column(Integer)                              # Día de la receta (ej: 1, 2, 3...)
    comida = Column(Enum("desayuno", "almuerzo", "cena", name="tipo_comida"))  # Tipo de comida
    nombre = Column(String)                            # Nombre de la receta
    ingredientes = Column(Text)                        # Ingredientes en texto
    preparacion = Column(Text)                         # Preparación en texto
    foto_url = Column(String)                          # URL de foto (opcional)

class ProgresoUsuario(Base):
    __tablename__ = "progreso_usuarios"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"))  # Relación con usuario
    peso = Column(Float)                                    # Peso registrado
    energia = Column(Integer)                               # Nivel de energía (ejemplo: 1-10)
    sueno = Column(Integer)                                 # Calidad de sueño (ejemplo: 1-10)
    comentarios = Column(Text)                              # Comentarios libres
    fecha = Column(DateTime, default=func.now())            # Fecha de registro, por defecto ahora
