from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()

@router.get("/setup-agregar-columnas")
def agregar_columnas_usuarios(db: Session = Depends(get_db)):
    try:
        db.execute(text("""
            ALTER TABLE usuarios
            ADD COLUMN IF NOT EXISTS telegram_id BIGINT UNIQUE,
            ADD COLUMN IF NOT EXISTS token VARCHAR UNIQUE,
            ADD COLUMN IF NOT EXISTS fecha_activacion TIMESTAMP,
            ADD COLUMN IF NOT EXISTS horario_envio TIME DEFAULT '08:00';
        """))
        db.commit()
        return {"status": "ok", "mensaje": "Columnas agregadas correctamente"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}
