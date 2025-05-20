from fastapi import FastAPI
from app.db.session import engine, Base        # <- instancia correcta
from app.models import alarma, dispositivo     # importa TODOS los modelos

# -------------  TABLAS -------------
Base.metadata.create_all(bind=engine)          # ahora sí usa el Engine real

# -------------  FASTAPI -------------
app = FastAPI()

from app.routers import alarma_router, iot_router
app.include_router(alarma_router.router, prefix="/alarma", tags=["Alarma"])
app.include_router(iot_router.router,   prefix="/iot",    tags=["IoT"])

@app.get("/")
def root():
    return {"message": "Backend de Domótica funcionando correctamente"}
