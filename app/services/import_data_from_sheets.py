import gspread
import os
import json
from google.oauth2.service_account import Credentials
from sqlalchemy.orm import Session
from app.models.receta import Receta
from app.models.mensaje import Mensaje
from app.models.plan import Plan

# 1. Configuración de credenciales
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
creds_dict = json.loads(os.getenv("GOOGLE_CREDS_JSON"))
credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(credentials)

# 2. Función para importar recetas
def importar_recetas(db: Session):
    try:
        spreadsheet = client.open("Programa 21 Días R2")
        sheet = spreadsheet.sheet1
        print("✅ Documento accedido:", spreadsheet.title)

        rows = sheet.get_all_values()
        encabezado = rows[0]

        # Detectar columnas de días e imágenes
        dias = []
        for i in range(2, len(encabezado), 2):  # Salta de 2 en 2 (día, imagen)
            dia_texto = encabezado[i]
            if "Día" in dia_texto or "Dia" in dia_texto:
                dia_num = int(dia_texto.replace("Día", "").replace("Dia", "").strip())
                dias.append((i, dia_num))  # (posición en la fila, número de día)

        recetas = []
        db.query(Receta).delete()  # Limpia la tabla antes

        for fila in rows[1:]:
            hora = fila[0]
            tipo_comida = fila[1]

            for col_index, dia_num in dias:
                titulo = fila[col_index].strip() if len(fila) > col_index and fila[col_index] else ""
                imagen_url = fila[col_index + 1].strip() if len(fila) > col_index + 1 and fila[col_index + 1] else ""

                if not titulo:
                    continue  # Saltar si no hay título

                receta = Receta(
                    dia=dia_num,
                    tipo_comida=tipo_comida,
                    hora=hora,
                    idioma="es",
                    titulo=titulo,
                    descripcion="",
                    ingredientes="",
                    instrucciones="",
                    imagen_url=imagen_url
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
