from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.session import engine, Base         
from app.models import alarma, dispositivo      
from app.seed_devices import run as run_seeder
from app.routers import alarma_router, iot_router

# -------------  TABLAS -------------
Base.metadata.create_all(bind=engine)

# -------------  LIFESPAN -------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔧 Ejecutando run_seeder()...")
    run_seeder()
    yield
    print("🛑 Apagando backend...")

# -------------  FASTAPI APP -------------
app = FastAPI(lifespan=lifespan)

# -------------  RUTAS -------------
app.include_router(alarma_router.router, prefix="/alarma", tags=["Alarma"])
app.include_router(iot_router.router, prefix="/iot", tags=["IoT"])

@app.get("/")
def root():
    return {"message": "Backend de Domótica funcionando correctamente"}