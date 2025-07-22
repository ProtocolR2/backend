from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.crud import user as user_crud
from app.database import get_db

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/registrar-usuario", response_model=UserOut)
def registrar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint que permite registrar un usuario con todos los datos completos.
    Utilizado por flujos con token/manual.
    """
    db_user = user_crud.get_user_by_telegram_id(db, user.telegram_id)
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario ya está registrado.")
    try:
        return user_crud.create_user(db, user)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

@router.post("/registrar-telegram")
def registrar_telegram(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint pensado para que la landing page registre solo con telegram_id, email y nombre.
    Si ya existe, no falla.
    """
    existing_user = user_crud.get_user_by_telegram_id(db, user_data.telegram_id)
    if existing_user:
        return {"status": "ok", "message": "Usuario ya registrado."}
    try:
        user_crud.create_user(db, user_data)
        return {"status": "ok", "message": "Usuario registrado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar usuario: {str(e)}")

@router.get("/{telegram_id}", response_model=UserOut)
def get_user(telegram_id: int, db: Session = Depends(get_db)):
    """
    Trae el usuario desde su Telegram ID. Usado por el bot.
    """
    db_user = user_crud.get_user_by_telegram_id(db, telegram_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return db_user
