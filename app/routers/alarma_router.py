
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.alarma import AlarmaCreate, AlarmaOut
from app.services.alarma_service import crear_alarma, obtener_alarmas

router = APIRouter()

@router.post("/configurar", response_model=AlarmaOut)
def configurar_alarma(alarma: AlarmaCreate, db: Session = Depends(get_db)):
    return crear_alarma(db, alarma)

@router.get("", response_model=list[AlarmaOut])
def listar_alarmas(db: Session = Depends(get_db)):
    return obtener_alarmas(db)