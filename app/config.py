import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://r2:H425iN91es9wnXG0n787h886CsjMm5gr@dpg-d1mlj0u3jp1c73dqtn7g-a.oregon-postgres.render.com/dbr2"
)

DEFAULT_LANGUAGE = "es"

# 🚀 Agregamos soporte para múltiples idiomas
IDIOMAS_SOPORTADOS = ["es", "en", "fr", "ru", "br"]  # Podés agregar más como "pt", "de", etc.
