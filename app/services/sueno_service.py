from datetime import datetime, timedelta, time as time_obj
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.alarma import Alarma
from app.models.sueno import Sueno
from app.schemas.sueno import SuenoIn

def calcular_sueno(db: Session, datos: SuenoIn):
    alarma = db.query(Alarma).filter(Alarma.id == datos.id).first()
    if not alarma:
        raise HTTPException(status_code=404, detail="Alarma no encontrada")

    hora_dormir = datetime.combine(datetime.today(), datos.hora_actual)
    hora_alarma = datetime.combine(datetime.today(), alarma.hora)

    if hora_alarma <= hora_dormir:
        hora_alarma += timedelta(days=1)

    duracion = hora_alarma - hora_dormir
    minutos = int(duracion.total_seconds() // 60)
    ciclos = minutos // 90

    sueno = Sueno(
        alarma_id=alarma.id,
        hora_dormir=datos.hora_actual,
        hora_alarma=alarma.hora,
        duracion_min=minutos,
        ciclos=ciclos,
    )
    db.add(sueno)
    db.commit()
    db.refresh(sueno)
    return sueno
