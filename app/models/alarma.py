from sqlalchemy import Column, Integer, Time, Boolean
from app.db.session import Base

class Alarma(Base):
    __tablename__ = "alarma"           
    id     = Column(Integer, primary_key=True, index=True)
    hora   = Column(Time, nullable=False)
    activa = Column(Boolean, default=True)
