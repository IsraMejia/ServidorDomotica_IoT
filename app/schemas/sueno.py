from pydantic import BaseModel
from datetime import time, datetime

class SuenoIn(BaseModel):
    id: int  # ID de la alarma
    hora_actual: time

class SuenoOut(BaseModel):
    id: int
    hora_dormir: time
    hora_alarma: time
    duracion_min: int
    ciclos: int
    fecha_registro: datetime

    class Config:
        orm_mode = True
