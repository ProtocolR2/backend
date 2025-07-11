import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy.orm import Session
from app.models.receta import Receta
from app.database import Base, engine

# URL del Google Sheet
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1IqZR9PbHGV-MjzVgOzbPwBQXVFHtQ-oEhxuVIgCECd0/edit?usp=sharing"

def importar_recetas(db: Session):
    # Crear la tabla si no existe
    Base.metadata.create_all(bind=engine)

    # Autenticación con Google
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
    client = gspread.authorize(creds)

    # Abrir hoja y obtener data
    sheet = client.open_by_url(SPREADSHEET_URL).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Procesar cada fila y guardar en DB
    for _, row in df.iterrows():
        dia = int(row["Día"])
        tipo = row["Tipo"]  # Breakfast, Lunch, Dinner
        nombre = row["Nombre"]
        ingredientes = row["Ingredientes"]
        instrucciones = row["Instrucciones"]

        # Armar imagen URL desde convención
        ext = "png" if tipo.lower() != "lunch" else "jpg"
        imagen_url = f"https://res.cloudinary.com/protocolr2/image/upload/{dia}_R2_{tipo}.{ext}"

        receta = Receta(
            dia=dia,
            tipo=tipo,
            nombre=nombre,
            ingredientes=ingredientes,
            instrucciones=instrucciones,
            imagen_url=imagen_url
        )
        db.add(receta)

    db.commit()
    return {"status": "ok", "mensaje": f"{len(df)} recetas importadas"}
