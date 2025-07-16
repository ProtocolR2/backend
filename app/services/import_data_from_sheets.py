iimport gspread
import os
import json
from google.oauth2.service_account import Credentials
from sqlalchemy.orm import Session
from app.models.receta import Receta
from app.models.mensaje import Mensaje
from app.models.plan import Plan
from app.database import Base, engine

# 1. Configuración de credenciales
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
creds_dict = json.loads(os.getenv("GOOGLE_CREDS_JSON"))
credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(credentials)

# 2. Función para importar recetas
def importar_recetas(db: Session):
    try:
        # Asegurarnos que la tabla tenga la estructura correcta

        Receta.__table__.drop(bind=engine, checkfirst=True)
        Base.metadata.create_all(bind=engine)

        spreadsheet = client.open("Programa 21 Días R2")
        sheet = spreadsheet.sheet1
        print("✅ Documento accedido:", spreadsheet.title)

        rows = sheet.get_all_values()
        encabezado = rows[0]
        dias = encabezado[2:]

        recetas = []

        for fila in rows[1:]:
            hora = fila[0] if fila[0] else ""
            tipo_comida = fila[1]

            for i in range(0, len(dias), 2):  # Día N y Día N img
                dia_str = dias[i].replace("Día ", "").replace("Dia ", "").strip()
                if not dia_str.isdigit():
                    continue

                dia_num = int(dia_str)
                titulo = fila[2 + i].strip() if 2 + i < len(fila) else ""
                imagen_url = fila[2 + i + 1].strip() if 2 + i + 1 < len(fila) else ""

                if not titulo:
                    continue  # Saltar si no hay título

                receta = Receta(
                    dia=dia_num,
                    hora=hora,
                    instancia=tipo_comida,
                    titulo=titulo,
                    imagen_url=imagen_url,
                    idioma="es"
                )
                db.add(receta)
                recetas.append(receta)

        db.commit()
        print(f"✅ Se importaron {len(recetas)} recetas desde Google Sheets")

    except Exception as e:
        print("❌ Error al importar recetas:", e)
        raise

# 3. Función para importar mensajes
def importar_mensajes(db: Session):
    try:
        spreadsheet = client.open("Mensajería R2_Bot")
        sheet = spreadsheet.sheet1
        print("✅ Documento accedido:", spreadsheet.title)

        data = sheet.get_all_records()

        db.query(Mensaje).delete()

        for row in data:
            mensaje = Mensaje(
                hora=row["hora"],
                tipo=row.get("tipo", "recordatorio"),
                idioma=row.get("idioma", "es"),
                contenido=row["contenido"]
            )
            db.add(mensaje)

        db.commit()
        print("✅ Mensajes importados con éxito")

    except Exception as e:
        print("❌ Error al importar mensajes:", e)
        raise

# 4. Función para importar planes
def importar_planes(db: Session):
    try:
        spreadsheet = client.open("Plan Mantenimiento 365")
        sheet = spreadsheet.sheet1
        print("✅ Documento accedido:", spreadsheet.title)

        data = sheet.get_all_records()

        db.query(Plan).delete()

        for row in data:
            plan = Plan(
                nombre=row["nombre"],
                duracion_dias=int(row["duracion_dias"]),
                descripcion=row.get("descripcion", ""),
                idioma=row.get("idioma", "es"),
            )
            db.add(plan)

        db.commit()
        print("✅ Planes importados con éxito")

    except Exception as e:
        print("❌ Error al importar planes:", e)
        raise

# 5. Función general para importar todo
def importar_todo_desde_sheets(db: Session):
    importar_recetas(db)
    importar_mensajes(db)
    importar_planes(db)
