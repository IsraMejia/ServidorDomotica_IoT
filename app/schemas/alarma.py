from pydantic import BaseModel
from datetime import time

class AlarmaCreate(BaseModel):
    hora: time
    activa: bool = True

class AlarmaOut(BaseModel):
    id: int
    hora: time
    activa: bool

    class Config:
        orm_mode = True