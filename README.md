# 🌐 SmartHome Backend - FastAPI

Este es el servidor backend del sistema embebido de domótica inteligente. Desarrollado con **FastAPI**, este servicio administra las alarmas, el control de dispositivos IoT y el cálculo de sueño del usuario. Toda la arquitectura está pensada para operar en red Wi-Fi local, garantizando independencia de servicios externos.

---

## 👨‍💻 Autores

- **Mejía Alba Israel Hipólito**
- **Ruiz Gaspar José Ángel**

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## ⚙️ Arquitectura y tecnologías

- **Framework principal:** FastAPI (Python 3.11+)
- **Base de datos:** PostgreSQL
- **Contenedorización:** Docker + Docker Compose
- **ORM:** SQLAlchemy
- **Documentación automática:** Swagger UI y Redoc
- **Lógica desacoplada:** Principios inspirados en Clean Architecture

## 📁 Estructura del proyecto

```
app/
├── db/                  # Configuración y sesión con la base de datos
├── models/              # Tablas: alarma, dispositivo, sueño
├── routers/             # Endpoints organizados por funcionalidad
├── services/            # Lógica principal (alarma, dispositivos, sueño)
├── seed_devices.py      # Seeder de dispositivos iniciales
└── main.py              # Configuración de FastAPI y lifespan
```

## 🔌 Endpoints principales

- `POST /alarma/configurar`: Crea o actualiza una alarma
- `GET /alarma`: Devuelve la alarma actual configurada
- `POST /iot/dispositivo`: Activa o desactiva un dispositivo por nombre
- `GET /informe`: Retorna informe diario de sueño y sensores
- `GET /estado`: Estado general del sistema (dispositivos, sensores, alarma)

> Todos los endpoints están documentados automáticamente en:  
> http://localhost:8000/docs

## 🚀 Puesta en marcha

1. Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/smarthome-backend.git
cd smarthome-backend
```

2. Copia el archivo `.env.example` a `.env` y ajusta variables como la IP del ESP32 y la base de datos.

3. Levanta los servicios con Docker:

```bash
docker-compose up --build
```

4. Accede al backend en:
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs

## 🧠 Funcionalidades destacadas

- Activación física remota de alarma (ventilador, buzzer, atomizador)
- Control total de dispositivos conectados al ESP32
- Almacenamiento persistente de alarmas y registros de sueño
- Arquitectura desacoplada, modular y mantenible
- Seeder automático de dispositivos al arrancar


 