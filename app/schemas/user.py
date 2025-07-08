from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    id: int
    first_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]
    email: Optional[str] = None

class UserOut(BaseModel):
    id: int
    first_name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    plan: str
    is_verified: bool

    class Config:
        orm_mode = True
