from fastapi import FastAPI
from app.routes import user

app = FastAPI(title="Protocolo R2 Backend")

# Incluir rutas del usuario
app.include_router(user.router)

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "🚀 Backend del Protocolo R2 en funcionamiento."}
