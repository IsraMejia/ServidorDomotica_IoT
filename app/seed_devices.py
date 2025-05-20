from app.db.session import SessionLocal
from app.models.dispositivo import DispositivoIoT

# Lista de dispositivos que quieres tener por defecto
dispositivos_iniciales = [
    {"nombre": "Ventilador", "estado": False, "tipo": "output"},
    {"nombre": "Servir_Agua", "estado": False, "tipo": "output"},
    {"nombre": "Atomizador", "estado": False, "tipo": "output"},
    {"nombre": "Puerta", "estado": False, "tipo": "output"},
]

def run():
    db = SessionLocal()
    for d in dispositivos_iniciales:
        existe = db.query(DispositivoIoT).filter_by(nombre=d["nombre"]).first()
        if not existe:
            nuevo = DispositivoIoT(**d)
            db.add(nuevo)
    db.commit()
    db.close()

if __name__ == "__main__":
    run()