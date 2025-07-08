import os
import psycopg2
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# --- Configuración de FastAPI ---
app = FastAPI()

# --- CORS (para permitir acceso del bot y futuro frontend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Conexión a PostgreSQL ---
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Falta la variable de entorno DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# --- Modelos de datos ---
class Usuario(BaseModel):
    telegram_id: int
    first_name: Optional[str] = ""
    username: Optional[str] = ""
    language_code: Optional[str] = "es"
    email: Optional[str] = ""
    plan: Optional[str] = "free"

# --- Endpoint de test (para UptimeRobot) ---
@app.get("/ping")
def ping():
    return {"status": "ok"}

# --- Obtener usuario por telegram_id ---
@app.get("/usuarios/{telegram_id}")
def obtener_usuario(telegram_id: int):
    cursor.execute("SELECT * FROM usuarios WHERE telegram_id = %s", (telegram_id,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "id": user[0],
        "telegram_id": user[1],
        "first_name": user[2],
        "username": user[3],
        "language_code": user[4],
        "email": user[5],
        "plan": user[6]
    }

# --- Registrar nuevo usuario ---
@app.post("/usuarios")
def registrar_usuario(usuario: Usuario):
    cursor.execute("SELECT * FROM usuarios WHERE telegram_id = %s", (usuario.telegram_id,))
    if cursor.fetchone():
        raise HTTPException(status_code=409, detail="Usuario ya existe")

    cursor.execute("""
        INSERT INTO usuarios (telegram_id, first_name, username, language_code, email, plan)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        usuario.telegram_id,
        usuario.first_name,
        usuario.username,
        usuario.language_code,
        usuario.email,
        usuario.plan
    ))
    conn.commit()
    return {"status": "ok", "message": "Usuario registrado"}
