
from fastapi import APIRouter, Depends, Request, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.services.import_data_from_sheets import (
    importar_todo_desde_sheets,   # importa recetas + mensajes + planes
    importar_recetas,
    importar_mensajes,
    importar_planes,
)
from app.services.backup_data import backup_todo, restaurar_todo_desde_backup
import os

router = APIRouter(prefix="/admin", tags=["admin"])

# ——————————————————————————————————————————————————————————
# Utilidad de seguridad
# ——————————————————————————————————————————————————————————
def verificar_autorizacion(request: Request):
    secret = request.headers.get("x-init-secret")
    if secret != os.getenv("INIT_SECRET"):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="No autorizado")

# ——————————————————————————————————————————————————————————
# ENDPOINT “TODO JUNTO”  (para reseto_total.sh)
# ——————————————————————————————————————————————————————————
@router.post("/importar-recetas")
def importar_todo_endpoint(request: Request, db: Session = Depends(get_db)):
    """
    IMPORTA recetas + mensajes + planes en una sola llamada.
    Usado por el script reseto_total.sh para reinicializar todo.
    """
    verificar_autorizacion(request)
    importar_todo_desde_sheets(db)
    return {"status": "✅ Recetas, mensajes y planes importados correctamente"}

# ——————————————————————————————————————————————————————————
# ENDPOINTS INDIVIDUALES
# ——————————————————————————————————————————————————————————
@router.post("/importar-recetas-solo")
def importar_recetas_endpoint(request: Request, db: Session = Depends(get_db)):
    verificar_autorizacion(request)
    importar_recetas(db)
    return {"status": "✅ Recetas importadas correctamente"}

@router.post("/importar-mensajes")
def importar_mensajes_endpoint(request: Request, db: Session = Depends(get_db)):
    verificar_autorizacion(request)
    importar_mensajes(db)
    return {"status": "✅ Mensajes importados correctamente"}

@router.post("/importar-planes")
def importar_planes_endpoint(request: Request, db: Session = Depends(get_db)):
    verificar_autorizacion(request)
    importar_planes(db)
    return {"status": "✅ Planes importados correctamente"}

# ——————————————————————————————————————————————————————————
# Importar solo recetas de mantenimiento (365 días)
# ——————————————————————————————————————————————————————————
@router.post("/importar-mantenimiento")
def importar_mantenimiento_endpoint(request: Request, db: Session = Depends(get_db)):
    """
    Importa las recetas del plan de mantenimiento 365 desde Google Sheets.
    Utiliza la pestaña horizontal. Salta celdas vacías.
    """
    from app.services.import_data_from_sheets import importar_recetas_mantenimiento

    verificar_autorizacion(request)
    importar_recetas_mantenimiento(db)
    return {"status": "✅ Recetas de mantenimiento importadas correctamente"}

# ——————————————————————————————————————————————————————————
# Gestión de tablas
# ——————————————————————————————————————————————————————————
@router.post("/init-db")
def init_db(request: Request):
    verificar_autorizacion(request)
    Base.metadata.create_all(bind=engine)
    return {"status": "✅ Tablas creadas correctamente"}

# ——————————————————————————————————————————————————————————
# Backup y restauración
# ——————————————————————————————————————————————————————————
@router.post("/backup")
def backup(request: Request, db: Session = Depends(get_db)):
    verificar_autorizacion(request)
    backup_todo(db)
    return {"status": "✅ Backup realizado correctamente"}

@router.post("/restaurar-backup")
def restaurar_backup(request: Request, db: Session = Depends(get_db)):
    verificar_autorizacion(request)
    restaurar_todo_desde_backup(db)
    return {"status": "✅ Datos restaurados desde backup local"}

# ------------- VISOR Y FILTROS RÁPIDOS -----------------
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy import func
from app.models.receta import Receta
from app.models.receta_mantenimiento import RecetaMantenimiento
from app.models.mensaje import Mensaje
from app.models.plan import Plan

# Helper para aplicar filtros comunes
def aplicar_filtros(query, modelo, dia: Optional[int], idioma: Optional[str], instancia: Optional[str]):
    if dia is not None and hasattr(modelo, "dia"):
        query = query.filter(modelo.dia == dia)
    if idioma is not None and hasattr(modelo, "idioma"):
        query = query.filter(modelo.idioma == idioma)
    if instancia is not None and hasattr(modelo, "instancia"):
        query = query.filter(modelo.instancia.ilike(f"%{instancia}%"))
    return query

# --------- Recetas 21 días ----------
@router.get("/visor/recetas", response_class=JSONResponse)
def visor_recetas(
    request: Request,
    dia: Optional[int] = None,
    idioma: Optional[str] = None,
    instancia: Optional[str] = None,
    db: Session = Depends(get_db),
):
    verificar_autorizacion(request)
    q = aplicar_filtros(db.query(Receta), Receta, dia, idioma, instancia).all()
    return [r.__dict__ for r in q]

# --------- Recetas Mantenimiento 365 ----------
@router.get("/visor/recetas-mantenimiento", response_class=JSONResponse)
def visor_recetas_mantenimiento(
    request: Request,
    dia: Optional[int] = None,
    idioma: Optional[str] = None,
    instancia: Optional[str] = None,
    db: Session = Depends(get_db),
):
    verificar_autorizacion(request)
    q = aplicar_filtros(db.query(RecetaMantenimiento), RecetaMantenimiento, dia, idioma, instancia).all()
    return [r.__dict__ for r in q]

# --------- Mensajes ----------
@router.get("/visor/mensajes", response_class=JSONResponse)
def visor_mensajes(
    request: Request,
    dia: Optional[int] = None,
    idioma: Optional[str] = None,
    db: Session = Depends(get_db),
):
    verificar_autorizacion(request)
    q = aplicar_filtros(db.query(Mensaje), Mensaje, dia, idioma, None).all()
    return [m.__dict__ for m in q]

# --------- Planes (meta) ----------
@router.get("/visor/planes", response_class=JSONResponse)
def visor_planes(request: Request, db: Session = Depends(get_db)):
    verificar_autorizacion(request)
    planes = db.query(Plan).all()
    return [p.__dict__ for p in planes]

# --------- Resumen / Conteo ----------
@router.get("/visor/resumen", response_class=JSONResponse)
def visor_resumen(request: Request, db: Session = Depends(get_db)):
    verificar_autorizacion(request)
    resumen = {
        "recetas_21d": db.query(func.count(Receta.id)).scalar(),
        "recetas_mantenimiento": db.query(func.count(RecetaMantenimiento.id)).scalar(),
        "mensajes": db.query(func.count(Mensaje.id)).scalar(),
        "planes": db.query(func.count(Plan.id)).scalar(),
    }
    return resumen


