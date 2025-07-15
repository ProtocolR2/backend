import os
import json
from sqlalchemy.orm import Session
from app.models.receta import Receta
from app.models.mensaje import Mensaje
from app.models.plan import Plan

BACKUP_DIR = "backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_tabla(db: Session, modelo, nombre_archivo):
    data = db.query(modelo).all()
    resultado = [obj.__dict__.copy() for obj in data]

    # Quitar claves internas como _sa_instance_state
    for r in resultado:
        r.pop("_sa_instance_state", None)

    path = os.path.join(BACKUP_DIR, nombre_archivo)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"🧾 Backup guardado: {path}")

def backup_todo(db: Session):
    backup_tabla(db, Receta, "recetas_backup.json")
    backup_tabla(db, Mensaje, "mensajes_backup.json")
    backup_tabla(db, Plan, "planes_backup.json")
