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
