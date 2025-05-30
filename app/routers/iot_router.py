from fastapi import APIRouter, Depends, HTTPException, requests
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.dispositivo import DispositivoUpdate, DispositivoOut
from app.services.dispositivo_service import actualizar_estado_dispositivo, obtener_dispositivos

router = APIRouter()



@router.get("/dispositivos", response_model=list[DispositivoOut])
def listar_dispositivos(db: Session = Depends(get_db)):
    return obtener_dispositivos(db)



@router.get("/sensor/temperatura")
def leer_temperatura():
    try:
        response = requests.get("http://192.168.1.60/temperatura", timeout=2)  # ESP32 #2
        return response.json()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="ESP32 no disponible")

 
    
@router.post("/dispositivo", response_model=DispositivoOut)
def cambiar_estado_dispositivo(data: DispositivoUpdate, db: Session = Depends(get_db)):
    return actualizar_estado_dispositivo(db, data.nombre, data.estado)
