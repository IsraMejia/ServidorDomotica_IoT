
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.alarma import AlarmaCreate, AlarmaOut, AlarmaUpdate
from app.schemas.sueno import SuenoIn, SuenoOut
from app.services.alarma_service import crear_alarma, desactivar_alarma, obtener_alarmas
from app.services.sueno_service import calcular_sueno

router = APIRouter()

@router.post("/configurar", response_model=AlarmaOut)
def configurar_alarma(alarma: AlarmaCreate, db: Session = Depends(get_db)):
    return crear_alarma(db, alarma)

@router.get("", response_model=list[AlarmaOut])
def listar_alarmas(db: Session = Depends(get_db)):
    return obtener_alarmas(db)

@router.post("/desactivar", response_model=AlarmaOut)
def desactivar(alarma: AlarmaUpdate, db: Session = Depends(get_db)):
    return desactivar_alarma(db, alarma)

@router.post("/calculoSueno", response_model=SuenoOut)
def calcular_sueno_endpoint(data: SuenoIn, db: Session = Depends(get_db)):
    return calcular_sueno(db, data)