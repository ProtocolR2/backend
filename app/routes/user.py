from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.crud import user as user_crud
from app.database import get_db

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/registrar-usuario", response_model=UserOut)
def registrar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si usuario ya existe por telegram_id o token
    db_user = user_crud.get_user_by_telegram_id(db, user.telegram_id)
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya está registrado.")
    # Crear nuevo usuario
    try:
        return user_crud.create_user(db, user)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error interno al crear usuario.")

@router.post("/actualizar-usuario", response_model=UserOut)
def actualizar_usuario(telegram_id: int, datos: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_telegram_id(db, telegram_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    try:
        return user_crud.update_user(db, db_user, datos)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error interno al actualizar usuario.")

@router.get("/{telegram_id}", response_model=UserOut)
def get_user(telegram_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_telegram_id(db, telegram_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return db_user
