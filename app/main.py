from fastapi import FastAPI
from app.routes import user
from app.routes import admin  # 👈 NUEVO: importamos las rutas admin
from app.routes import visualizacion # ver las tablas en postman

app.include_router(visualizacion.router)

app = FastAPI(title="Protocolo R2 Backend")

# Incluir rutas del usuario
app.include_router(user.router)

# Incluir rutas administrativas (importar recetas)
app.include_router(admin.router)  # 👈 NUEVO: incluimos las rutas admin

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "🚀 Backend del Protocolo R2 en funcionamiento."}
