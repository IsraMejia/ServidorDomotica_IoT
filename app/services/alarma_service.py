from sqlalchemy.orm import Session
from app.models.alarma import Alarma
from app.schemas.alarma import  AlarmaCreate, AlarmaUpdate

def crear_alarma(db: Session, alarma: AlarmaCreate):
    db_alarma = Alarma(hora=alarma.hora, activa=alarma.activa)
    db.add(db_alarma)
    db.commit()
    db.refresh(db_alarma)
    return db_alarma

def obtener_alarmas(db: Session):
    return db.query(Alarma).all()

def desactivar_alarma(db: Session, alarma_data: AlarmaUpdate):
    db_alarma = db.query(Alarma).filter(Alarma.id == alarma_data.id).first()
    if not db_alarma:
        raise Exception("Alarma no encontrada")

    db_alarma.hora = alarma_data.hora
    db_alarma.activa = alarma_data.activa
    db.commit()
    db.refresh(db_alarma)
    return db_alarma
