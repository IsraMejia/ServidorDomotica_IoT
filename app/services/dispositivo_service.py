from sqlalchemy.orm import Session
import requests
from fastapi import HTTPException
from app.models.dispositivo import DispositivoIoT

# Mapeo entre dispositivos y rutas en ESP32
DISPOSITIVOS_ESP32 = {
    "Ventilador": {
        "url": "http://192.168.4.10/ventilador",  # ESP32 #1
        "metodo": "post"
    },
    "Servir_Agua": {
        "url": "http://192.168.4.10/bomba",       # ESP32 #1
        "metodo": "post"
    },
    "Atomizador": {
        "url": "http://192.168.4.11/atomizador",       # ESP32 #2
        "metodo": "post"
    },
    "Puerta": {
        "url": "http://192.168.4.11/puerta",       # ESP32 #2
        "metodo": "post"
    }
    #TODO : Agregar al ESP32 2 que reciba la peticion de encender alarma, el servidor solito ira reconociendo la hora actual y verifica si hay una alarma que coincida, en caso de que esto sea cierto , dispara la peticion de encender alarma la ESP32 procesa la alarma para que suene un buzzer y se apague con un boton
    # El sensor de temperatura se lee desde otro endpoint, no se activa.
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
