from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.receta import Receta
from app.models.mensaje import Mensaje
from app.models.receta_mantenimiento import RecetaMantenimiento
from app.models.plan import Plan

router = APIRouter(prefix="/resumen", tags=["resumen"])

@router.get("/")
def obtener_resumen(db: Session = Depends(get_db)):
    resumen = {
        "recetas_cargadas": db.query(Receta).count(),
        "mensajes_cargados": db.query(Mensaje).count(),
        "recetas_mantenimiento": db.query(RecetaMantenimiento).count(),
        "planes": db.query(Plan).count(),
    }
    return resumen
