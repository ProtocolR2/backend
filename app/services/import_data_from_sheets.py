import gspread
import os
import json
from google.oauth2.service_account import Credentials
from sqlalchemy.orm import Session
from app.models.receta import Receta
from app.models.mensaje import Mensaje
from app.models.plan import Plan
from app.database import Base, engine
from app.config import IDIOMAS_SOPORTADOS

# ------------------------------------------
# 1. Configuración de Google Sheets
# ------------------------------------------

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Cargar credenciales del entorno (variable: GOOGLE_CREDS_JSON)
creds_dict = json.loads(os.getenv("GOOGLE_CREDS_JSON"))
credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(credentials)

# ------------------------------------------
# 2. Importar Recetas (usando ID de hoja)
# ------------------------------------------

def importar_recetas(db: Session):
    try:
        # Reinicia la tabla (DROP + CREATE)
        Receta.__table__.drop(bind=engine, checkfirst=True)
        Base.metadata.create_all(bind=engine)

        # Abre la hoja usando el ID (variable: SHEET_ID_RECETAS)
        sheet_id = os.getenv("SHEET_ID_RECETAS")
        spreadsheet = client.open_by_key(sheet_id)
        print("✅ Documento accedido:", spreadsheet.title)
        sheet = spreadsheet.sheet1

        rows = sheet.get_all_values()
        encabezado = rows[0]
        dias = encabezado[2:]  # columnas a partir de la tercera

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
                    continue  # salta si está vacío

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

# ------------------------------------------
# 3. Importar Mensajes
# ------------------------------------------

def importar_mensajes(db: Session):
    try:
        # 💥 Elimina y recrea la tabla mensajes (estructura actualizada del modelo)
        Mensaje.__table__.drop(bind=engine, checkfirst=True)
        Base.metadata.create_all(bind=engine)
        
        # Abre la hoja usando el ID (variable: SHEET_ID_MENSAJES)
        sheet_id = os.getenv("SHEET_ID_MENSAJES")
        spreadsheet = client.open_by_key(sheet_id)
        print("✅ Documento accedido:", spreadsheet.title)
        sheet = spreadsheet.sheet1

        data = sheet.get_all_records()
        mensajes = []

        for row in data:
            if row.get("activo", "").strip().lower() == "sí":
                try:
                    idioma = row.get("idioma", "es").strip().lower()
                    if idioma not in IDIOMAS_SOPORTADOS:
                        print(f"⚠️ Idioma no soportado: {idioma} en fila {row}")
                        continue

                    mensaje = Mensaje(
                        dia=int(row["día"]),
                        hora=row["hora"],
                        idioma=idioma,
                        contenido=row["mensaje"]
                    )
                    mensajes.append(mensaje)
                except Exception as e:
                    print(f"❌ Error al procesar fila: {row} - {e}")

        if mensajes:
            db.query(Mensaje).delete()
            db.add_all(mensajes)
            db.commit()
            print(f"✅ Se importaron {len(mensajes)} mensajes")
        else:
            print("⚠️ No se importaron mensajes (ninguno marcado como 'sí')")

    except Exception as e:
        print("❌ Error al importar mensajes:", e)
        raise

# ------------------------------------------
# 4. Importar Planes (Plan Mantenimiento 365)
# ------------------------------------------

def importar_planes(db: Session):
    try:
        # Abre la hoja usando el ID (variable: SHEET_ID_PLANES)
        sheet_id = os.getenv("SHEET_ID_PLANES")
        spreadsheet = client.open_by_key(sheet_id)
        print("✅ Documento accedido:", spreadsheet.title)
        sheet = spreadsheet.sheet1

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

# ------------------------------------------
# 6. Función para importar Plan Mantenimiento 365
# ------------------------------------------

def importar_recetas_mantenimiento(db: Session):
    """
    Importa el Plan Mantenimiento 365 (formato horizontal) a la tabla recetas_mantenimiento.
    Salta celdas sin título, así puedes ir completando la hoja de a poco.
    """
    try:
        # ¡Borramos y recreamos la tabla!
        from app.models.receta_mantenimiento import RecetaMantenimiento
        RecetaMantenimiento.__table__.drop(bind=engine, checkfirst=True)
        Base.metadata.create_all(bind=engine)

        sheet_id = os.getenv("SHEET_ID_PLANES")  # MISMA hoja que ya tienes, solo otra pestaña
        spreadsheet = client.open_by_key(sheet_id)
        sheet = spreadsheet.sheet1
        print("✅ Documento accedido:", spreadsheet.title)

        rows = sheet.get_all_values()
        encabezado = rows[0]            # Instancia | Día 1 | Día 1 Img | Día 2 | Día 2 Img | …
        dias = encabezado[1:]           # desde la segunda columna

        recetas = []

        for fila in rows[1:]:
            instancia = fila[0] or ""   # Columna A
            # si la fila está vacía, seguimos
            if not instancia.strip():
                continue

            for i in range(0, len(dias), 2):  # Día N y Día N Img
                dia_label = dias[i]
                if not dia_label.startswith("Día"):
                    continue

                dia_num = int(dia_label.replace("Día", "").strip())
                titulo = fila[1 + i].strip() if 1 + i < len(fila) else ""
                imagen_url = fila[1 + i + 1].strip() if 1 + i + 1 < len(fila) else ""

                # Salta si el título está vacío (aún no completaste esa celda)
                if not titulo:
                    continue

                # Puedes parsear hora a partir de instancia o ponerla vacía por ahora
                receta = RecetaMantenimiento(
                    dia=dia_num,
                    hora="",                     # Poner hora si la incluyes en otra columna
                    instancia=instancia,
                    titulo=titulo,
                    imagen_url=imagen_url,
                    idioma="es"
                )
                db.add(receta)
                recetas.append(receta)

        db.commit()
        print(f"✅ Se importaron {len(recetas)} recetas de mantenimiento")

    except Exception as e:
        print("❌ Error al importar mantenimiento:", e)
        raise

# ------------------------------------------
# 7. Función general para importar todo
# Usada por el endpoint /admin/importar-recetas (total)
# ------------------------------------------

def importar_todo_desde_sheets(db: Session):
    importar_recetas(db)
    importar_mensajes(db)
    importar_planes(db)
    importar_recetas_mantenimiento(db)
