from sqlalchemy.orm import Session
from app.models.alarma import Alarma
from app.schemas.alarma import AlarmaCreate

def crear_alarma(db: Session, alarma: AlarmaCreate):
    db_alarma = Alarma(hora=alarma.hora, activa=alarma.activa)
    db.add(db_alarma)
    db.commit()
    db.refresh(db_alarma)
    return db_alarma

def obtener_alarmas(db: Session):
    return db.query(Alarma).all()