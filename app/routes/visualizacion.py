# Este archivo sirve para ver en postman las tablas de manera linda
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.receta import Receta
from app.models.mensaje import Mensaje
from app.models.receta_mantenimiento import RecetaMantenimiento

router = APIRouter(prefix="", tags=["visualizacion"])

# 🥗 Recetas 21 días
@router.get("/recetas/")
def ver_recetas(dia: Optional[int] = None, idioma: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Receta)
    if dia:
        query = query.filter(Receta.dia == dia)
    if idioma:
        query = query.filter(Receta.idioma == idioma)
    return query.all()

# 💬 Mensajes
@router.get("/mensajes/")
def ver_mensajes(dia: Optional[int] = None, idioma: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Mensaje)
    if dia:
        query = query.filter(Mensaje.dia == dia)
    if idioma:
        query = query.filter(Mensaje.idioma == idioma)
    return query.all()

# 🔄 Recetas de mantenimiento (Plan 365)
@router.get("/mantenimiento/")
def ver_mantenimiento(dia: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(RecetaMantenimiento)
    if dia:
        query = query.filter(RecetaMantenimiento.dia == dia)
    return query.all()
