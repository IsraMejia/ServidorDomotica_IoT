from sqlalchemy import Column, Integer, Time, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.session import Base

class Sueno(Base):
    __tablename__ = "sueno"

    id = Column(Integer, primary_key=True, index=True)
    alarma_id = Column(Integer, ForeignKey("alarma.id"))
    hora_dormir = Column(Time, nullable=False)
    hora_alarma = Column(Time, nullable=False)
    duracion_min = Column(Integer)
    ciclos = Column(Integer)
    fecha_registro = Column( DateTime, default=lambda: datetime.now(timezone.utc) )

    alarma = relationship("Alarma")
