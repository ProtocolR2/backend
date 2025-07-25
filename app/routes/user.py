from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from app.schemas.user import UserCreate, UserOut
from app.crud import user as user_crud
from app.database import get_db
from datetime import datetime

router = APIRouter(prefix="/api/users", tags=["users"])

# 🔗 URL de la landing para pago (modificable desde un solo lugar)
LANDING_R2 = "https://tulanding.com/r2"  # ✅ CAMBIAR ESTA URL cuando esté la definitiva

# 🔐 Modelo para activación por token
class TokenActivationRequest(BaseModel):
    telegram_id: int
    token: str


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
        # Aseguramos campos nuevos por defecto
        if not user_data.plan:
            user_data.plan = "free"
        if not user_data.programas_activos:
            user_data.programas_activos = ["R2"]
        user_crud.create_user(db, user_data)
        return {"status": "ok", "message": "Usuario registrado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar usuario: {str(e)}")


@router.post("/activar")
def activar_usuario(data: TokenActivationRequest, db: Session = Depends(get_db)):
    """
    Activa un usuario por token si es válido y coincide con su telegram_id.
    """
    user = user_crud.get_user_by_token(db, data.token)

    if not user:
        raise HTTPException(status_code=404, detail="Token inválido o ya utilizado")

    if user.telegram_id != data.telegram_id:
        raise HTTPException(status_code=400, detail="Token no corresponde a este usuario")

    if user.is_verified:
        return {"status": "ok", "message": "Usuario ya estaba activado."}

    user_crud.activate_user(db, user)
    return {"status": "ok", "message": "Usuario activado correctamente"}


@router.post("/notificar-usuarios-inactivos")
def notificar_usuarios_lentos(db: Session = Depends(get_db)):
    hoy = datetime.utcnow()
    mensajes_enviados = []

    usuarios = db.query(user_crud.User).filter(user_crud.User.fecha_activacion.isnot(None)).all()

    for usuario in usuarios:
        dias_usados = (hoy - usuario.fecha_activacion).days

        if dias_usados in [5, 10, 15, 20, 30, 40, 50]:
            mensajes_enviados.append({
                "telegram_id": usuario.telegram_id,
                "mensaje": (
                    f"Hola {usuario.first_name}, ¡vamos que podés! Hace {dias_usados} días que activaste el protocolo R2 y aún no avanzaste. "
                    f"Recordá que tenés 60 días para completarlo. 💪"
                )
            })
        elif dias_usados == 55:
            mensajes_enviados.append({
                "telegram_id": usuario.telegram_id,
                "mensaje": (
                    f"Hola {usuario.first_name}, tu acceso al Protocolo R2 vence en 5 días. ¡Aprovechá al máximo este tiempo! 🚀"
                )
            })
        elif dias_usados == 60:
            mensajes_enviados.append({
                "telegram_id": usuario.telegram_id,
                "mensaje": (
                    "⏳ Tu acceso al Protocolo R2 ha vencido (pasaron 60 días desde que lo activaste).\n\n"
                    "🎁 Pero no todo está perdido. Te ofrecemos acceso preferencial al nuevo plan de Mantenimiento 365. "
                    f"Accedé desde aquí 👉 {LANDING_R2}"
                )
            })

    return {"status": "ok", "mensajes": mensajes_enviados}
