from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Time, DateTime
from app.database import Base

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
    email = Column(String, nullable=True)
    plan = Column(String, default="free")
    is_verified = Column(Boolean, default=False)

    # Nuevos campos para onboarding y seguimiento
    telegram_id = Column(BigInteger, unique=True, nullable=True)
    token = Column(String, unique=True, nullable=True)
    fecha_activacion = Column(DateTime, nullable=True)
    horario_envio = Column(Time, default="08:00", nullable=True)
