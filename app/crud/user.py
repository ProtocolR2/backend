# ✅ backend/app/crud/user.py

import logging
from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

logger = logging.getLogger(__name__)


def get_user_by_telegram_id(db: Session, telegram_id: int):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()


def get_user_by_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.token == token).first()


def create_user(db: Session, user: schemas.UserCreate):
    # Generar cliente_id automático tipo R20001
    last_user = db.query(models.User).order_by(models.User.id.desc()).first()
    next_number = 1 if not last_user else last_user.id + 1
    cliente_id = f"R2{next_number:04d}"

    db_user = models.User(
        telegram_id=user.telegram_id,
        first_name=user.first_name,
        username=user.username,
        language_code=user.language_code,
        email=user.email,
        plan=user.plan or "free",
        is_verified=user.is_verified or False,
        token=user.token,
        fecha_activacion=user.fecha_activacion,
        horario_envio=user.horario_envio,
        cliente_id=cliente_id,
        programas_activos=user.programas_activos or ["R2"],
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creando usuario en DB: {e}")
        raise


def update_user(db: Session, db_user: models.User, user_update: schemas.UserUpdate):
    if user_update.first_name is not None:
        db_user.first_name = user_update.first_name
    if user_update.horario_envio is not None:
        db_user.horario_envio = user_update.horario_envio
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error actualizando usuario en DB: {e}")
        raise


def activate_user(db: Session, user: models.User):
    user.is_verified = True
    user.fecha_activacion = datetime.utcnow()
    user.token = None
    try:
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error activando usuario: {e}")
        raise
