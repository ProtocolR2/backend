from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, time

class UserBase(BaseModel):
    telegram_id: int
    first_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = "es"
    email: Optional[EmailStr] = None
    plan: Optional[str] = "free"
    is_verified: Optional[bool] = False
    token: Optional[str] = None
    fecha_activacion: Optional[datetime] = None
    horario_envio: Optional[time] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    horario_envio: Optional[time] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Para Pydantic v2

class UserOut(UserInDB):
    pass
