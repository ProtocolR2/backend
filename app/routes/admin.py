from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.import_recipes import importar_recetas

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/importar-recetas")
def importar(db: Session = Depends(get_db)):
    return importar_recetas(db)
