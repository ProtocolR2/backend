from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.crud import user as user_crud
from app.database import get_db

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si usuario ya existe
    db_user = user_crud.get_user_by_telegram_id(db, user.telegram_id)
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya está registrado.")
    # Crear nuevo usuario
    return user_crud.create_user(db, user)

@router.get("/{telegram_id}", response_model=UserOut)
def get_user(telegram_id: int, db: Session = Depends(get_db)):
    # Buscar usuario por telegram_id
    db_user = user_crud.get_user_by_telegram_id(db, telegram_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return db_user
