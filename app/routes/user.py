from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.crud.user import get_user, create_user
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = get_user(db, user.id)
    if existing:
        return existing
    return create_user(db, user)
