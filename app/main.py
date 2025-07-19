from fastapi import FastAPI
from app.routes import user
from app.routes import admin
from app.routes import visualizacion
from app.routes import resumen

# Nueva línea para setup
from app.routes import setup  

app = FastAPI(title="Protocolo R2 Backend")
app.include_router(resumen.router)
app.include_router(visualizacion.router)
app.include_router(user.router)
app.include_router(admin.router)

# Agregar setup router
app.include_router(setup.router)

@app.get("/")
def read_root():
    return {"message": "🚀 Backend del Protocolo R2 en funcionamiento."}
