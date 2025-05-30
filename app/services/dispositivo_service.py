from sqlalchemy.orm import Session
import requests
from fastapi import HTTPException
from app.models.dispositivo import DispositivoIoT

#BaseOptions(baseUrl: 'http://192.168.1.131:8000')
# '192.168.1.10' 
# Mapeo entre dispositivos y rutas en ESP32
DISPOSITIVOS_ESP32 = {
    "Ventilador": {
        # "url": "http://192.168.1.10/ventilador",  # ESP32 #1
        "url": "http://192.168.0.60/ventilador",  # ESP32 #1
        "metodo": "post"
    },
    "Servir_Agua": {
        # "url": "http://192.168.1.10/bomba",       # ESP32 #1
        "url": "http://192.168.0.60/bomba",
        "metodo": "post"
    }, 

    "Atomizador": {
        #"url": "http://192.168.1.10/atomizador",       # ESP32 #1 
        "url": "http://192.168.0.60/atomizador",       # ESP32 #1 
        "metodo": "post"
    },
    "Puerta": {
        # "url": "http://192.168.1.10/puerta",       # ESP32 #1
        "url": "http://192.168.0.60/puerta",       # ESP32 #1
        "metodo": "post"
    },
    "Alarma": {
        # "url": "http://192.168.1.10/puerta",       # ESP32 #1
        "url": "http://192.168.0.60/alarma",       # ESP32 #1
        "metodo": "post"
    } 
}



def enviar_orden_a_esp32(nombre: str, estado: bool):
    dispositivo = DISPOSITIVOS_ESP32.get(nombre)
    if not dispositivo:
        print(f"[DEBUG] Dispositivo '{nombre}' no está mapeado a un ESP32")
        return

    url = dispositivo["url"]
    print(f"[DEBUG] Enviando  a ESP32: {url} con estado={estado}")
    try:
        response = requests.post(url, json={"estado": estado}, timeout=2)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Falló el POST a {url}: {e}")
        # Solo logea, no interrumpe el flujo



def actualizar_estado_dispositivo(db: Session, nombre: str, estado: bool):
    dispositivo = db.query(DispositivoIoT).filter_by(nombre=nombre).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    dispositivo.estado = estado
    db.commit()
    db.refresh(dispositivo)

    # Esta llamada ya no puede romper el flujo
    enviar_orden_a_esp32(nombre, estado)

    return dispositivo


def obtener_dispositivos(db: Session):
    return db.query(DispositivoIoT).all()
