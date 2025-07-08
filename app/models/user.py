from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    username = Column(String)
    language_code = Column(String)
    email = Column(String, nullable=True)
    plan = Column(String, default="free")
    is_verified = Column(Boolean, default=False)
