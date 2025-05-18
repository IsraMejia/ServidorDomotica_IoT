from pydantic import BaseModel

class DispositivoUpdate(BaseModel):
    nombre: str
    estado: bool

class DispositivoOut(BaseModel):
    id: int
    nombre: str
    estado: bool
    tipo: str

    class Config:
        orm_mode = True
