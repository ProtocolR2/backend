import logging
from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

logger = logging.getLogger(__name__)

def get_user_by_telegram_id(db: Session, telegram_id: int):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        telegram_id=user.telegram_id,
        first_name=user.first_name,
        username=user.username,
        language_code=user.language_code,
        email=user.email,
        plan=user.plan,
        is_verified=user.is_verified,
        token=user.token,
        fecha_activacion=user.fecha_activacion,
        horario_envio=user.horario_envio,
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
