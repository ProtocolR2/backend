from fastapi import FastAPI
from app.routes import user
from app.routes import admin  # 👈 NUEVO: importamos las rutas admin

app = FastAPI(title="Protocolo R2 Backend")

# Incluir rutas del usuario
app.include_router(user.router)

# Incluir rutas administrativas (importar recetas)
app.include_router(admin.router)  # 👈 NUEVO: incluimos las rutas admin

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "🚀 Backend del Protocolo R2 en funcionamiento."}
