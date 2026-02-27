# Usa la imagen oficial de Python ligera
FROM python:3.11-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes como psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .

# Exponer el puerto (Railway lo ignora pero es buena práctica)
EXPOSE 8080

# El comando de inicio para FastAPI usando Uvicorn
# Railway inyectará la variable $PORT automáticamente
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
