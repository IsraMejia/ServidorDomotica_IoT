from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base

class DispositivoIoT(Base):
    __tablename__ = "dispositivo_iot"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)  # Ej: "Ventilador"
    estado = Column(Boolean, default=False)               # True = encendido
    tipo = Column(String, default="output")               # output o sensor
