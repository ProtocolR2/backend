from app.api.routes import setup  # 👈 importar el módulo

api_router.include_router(setup.router)  # 👈 agregar el router
