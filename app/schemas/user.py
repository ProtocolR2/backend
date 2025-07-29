from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, time

class UserBase(BaseModel):
    first_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]
    email: Optional[str]
    plan: Optional[str] = "free"
    is_verified: Optional[bool] = False
    telegram_id: Optional[int]
    token: Optional[str]
    fecha_activacion: Optional[datetime]
    horario_envio: Optional[time]
    cliente_id: Optional[str]
    programas_activos: Optional[List[str]] = ["R2"]

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    first_name: Optional[str]
    horario_envio: Optional[time]

class User(UserBase):
    id: int
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

UserInDB = User
