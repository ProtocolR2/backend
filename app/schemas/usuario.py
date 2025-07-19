from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import time, datetime

class UserBase(BaseModel):
    first_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    email: Optional[EmailStr] = None
    plan: Optional[str] = "free"
    is_verified: Optional[bool] = False
    telegram_id: Optional[int] = None
    token: Optional[str] = None
    fecha_activacion: Optional[datetime] = None
    horario_envio: Optional[time] = None

class UserCreate(UserBase):
    # Para crear usuario, token y telegram_id deberían llegar obligatorios
    telegram_id: int
    token: str

class UserUpdate(BaseModel):
    # Campos que se pueden actualizar desde bot (nombre, horario)
    first_name: Optional[str] = None
    horario_envio: Optional[time] = None

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
