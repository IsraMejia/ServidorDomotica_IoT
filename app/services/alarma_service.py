from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.alarma import Alarma
from app.schemas.alarma import AlarmaCreate, AlarmaUpdate
from sqlalchemy.exc import SQLAlchemyError

def crear_alarma(db: Session, alarma: AlarmaCreate):
    try:
        nueva = Alarma(hora=alarma.hora, activa=alarma.activa)
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva
    except SQLAlchemyError as e:
        db.rollback()
        print(f"⚠️ Error en crear_alarma: {e}")
        raise HTTPException(status_code=500, detail="Error al guardar la alarma")

def obtener_alarmas(db: Session):
    return db.query(Alarma).all()

def desactivar_alarma(db: Session, alarma_data: AlarmaUpdate):
    print(f"[DEBUG] Intentando desactivar la alarma con ID: {alarma_data.id}, hora: {alarma_data.hora}, activa: {alarma_data.activa}")

    db_alarma = db.query(Alarma).filter(Alarma.id == alarma_data.id).first()

    if not db_alarma:
        print(f"[ERROR] No se encontró la alarma con ID {alarma_data.id}")
        raise HTTPException(status_code=404, detail="Alarma no encontrada")

    db_alarma.hora = alarma_data.hora
    db_alarma.activa = alarma_data.activa

    db.commit()
    db.refresh(db_alarma)

    print(f"[SUCCESS] Alarma {db_alarma.id} desactivada correctamente")
    return db_alarma
