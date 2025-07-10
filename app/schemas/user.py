from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    telegram_id: int
    first_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = "es"
    email: Optional[EmailStr] = None
    plan: Optional[str] = "free"
    is_verified: Optional[bool] = False

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 reemplaza orm_mode

class UserOut(UserInDB):
    pass
