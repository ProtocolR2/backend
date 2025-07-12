from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from app.database import get_db, Base, engine
from app.services.import_recipes import importar_recetas
from app.models import receta, mensaje  # asegurate de importar todos los modelos que querés crear

import os

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/importar-recetas")
def importar(db: Session = Depends(get_db)):
    return importar_recetas(db)

@router.post("/init-db")
async def init_db(request: Request):
    secret = request.headers.get("x-init-secret")
    if secret != os.getenv("INIT_SECRET"):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="No autorizado")

    Base.metadata.create_all(bind=engine)
    return {"status": "✅ Tablas creadas correctamente"}
