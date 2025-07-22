from fastapi import FastAPI
from app.routes import user
from app.routes import admin
from app.routes import visualizacion
from app.routes import resumen
from app.routes import setup
from app.routes import mensajes  

app = FastAPI(title="Protocolo R2 Backend")

# ✅ Incluí todos los routers ordenados acá
app.include_router(resumen.router)
app.include_router(visualizacion.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(setup.router)
app.include_router(mensajes.router)  

@app.get("/")
def read_root():
    return {"message": "🚀 Backend del Protocolo R2 en funcionamiento."}
