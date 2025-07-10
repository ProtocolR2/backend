import logging
from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy.exc import SQLAlchemyError

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
