from sqlalchemy import Column, Integer, String, Boolean, BigInteger, Time, DateTime, ARRAY
from app.database import Base
import datetime

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
    email = Column(String, nullable=True)
    plan = Column(String, default="free")
    is_verified = Column(Boolean, default=False)

    telegram_id = Column(BigInteger, unique=True, nullable=True)
    token = Column(String, unique=True, nullable=True)
    fecha_activacion = Column(DateTime, nullable=True)
    horario_envio = Column(Time, default=datetime.time(8, 0), nullable=True)

    # 🆕 Nuevos campos
    cliente_id = Column(String, unique=True, nullable=True, index=True)
    programas_activos = Column(ARRAY(String), default=["R2"])

    def __repr__(self):
        return f"<User id={self.id} telegram_id={self.telegram_id} username={self.username}>"
