from fastapi import FastAPI
from app.routers import alarma_router

app = FastAPI()

# Rutas principales
app.include_router(alarma_router.router, prefix="/alarma", tags=["Alarma"])

@app.get("/")
def root():
    return {"message": "Backend de Domótica funcionando correctamente"}