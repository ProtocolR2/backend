import gspread
import os
import json
from google.oauth2.service_account import Credentials
from sqlalchemy.orm import Session
from app.models.receta import Receta

# Configuración de credenciales
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds_dict = json.loads(os.getenv("GOOGLE_CREDS_JSON"))
credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(credentials)

def importar_recetas(db: Session):
    try:
        spreadsheet = client.open("Programa 21 Días R2")
        sheet = spreadsheet.sheet1
        print(f"✅ Documento accedido: {spreadsheet.title}")

        data = sheet.get_all_values()
        headers = data[0]  # Fila 1: encabezados
        rows = data[1:]    # Resto: filas de recetas

        # Normalizar nombres de columna (e.g. "Día 1", "Dia 1 img")
        normalized_headers = [h.replace("Dia", "Día").strip() for h in headers]

        # Mapear columnas de cada día
        dias = []
        for i, h in enumerate(normalized_headers):
            if h.startswith("Día") and not h.endswith("img"):
                numero_dia = int(h.split(" ")[1])
                col_receta = i
                col_img = None

                # Buscar si la siguiente columna es la imagen
                if i + 1 < len(normalized_headers):
                    next_col = normalized_headers[i + 1]
                    if next_col == f"Día {numero_dia} img":
                        col_img = i + 1

                dias.append({"dia": numero_dia, "col_receta": col_receta, "col_img": col_img})

        # Borrar recetas anteriores
        db.query(Receta).delete()

        for row in rows:
            hora = row[0]
            instancia = row[1]

            for d in dias:
                titulo = row[d["col_receta"]].strip() if d["col_receta"] < len(row) else ""
                imagen_url = row[d["col_img"]].strip() if d["col_img"] and d["col_img"] < len(row) else ""

                if titulo:  # Si hay receta, guardar
                    receta = Receta(
                        dia=d["dia"],
                        hora=hora,
                        instancia=instancia,
                        titulo=titulo,
                        imagen_url=imagen_url,
                        idioma="es"  # Por ahora sólo español
                    )
                    db.add(receta)

        db.commit()
        print("✅ Recetas importadas con éxito")

    except Exception as e:
        print("❌ Error al importar recetas:", e)
        raise
