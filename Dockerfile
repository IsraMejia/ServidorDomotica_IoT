# Dockerfile
FROM python:3.10-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos de dependencias primero (mejor cache)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código al contenedor
COPY ./app ./app

# Expone el puerto donde corre Uvicorn
EXPOSE 8000

# Comando por defecto al iniciar el contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


