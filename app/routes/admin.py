from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from app.database import get_db, Base, engine
from app.models import receta, mensaje, plan
from app.services.import_data_from_sheets import importar_todo_desde_sheets

import os

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/importar-recetas")
def importar_recetas(request: Request, db: Session = Depends(get_db)):
    secret = request.headers.get("x-init-secret")
    if secret != os.getenv("INIT_SECRET"):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="No autorizado")

    importar_todo_desde_sheets(db)
    return {"status": "✅ Datos importados correctamente desde Google Sheets"}

@router.post("/init-db")
async def init_db(request: Request):
    secret = request.headers.get("x-init-secret")
    if secret != os.getenv("INIT_SECRET"):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="No autorizado")

    Base.metadata.create_all(bind=engine)
    return {"status": "✅ Tablas creadas correctamente"}
