from fastapi import FastAPI
from app.routers import alarma_router, iot_router

app = FastAPI()

# Rutas principales
app.include_router(alarma_router.router, prefix="/alarma", tags=["Alarma"])
app.include_router(iot_router.router, prefix="/iot", tags=["IoT"])

@app.get("/")
def root():
    return {"message": "Backend de Domótica funcionando correctamente"}