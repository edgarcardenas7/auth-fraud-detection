# Usa Python 3.11 (más estable que 3.14 para producción)
FROM python:3.11-slim

# Metadata
LABEL maintainer="edgar@example.com"
LABEL description="Auth & Fraud Detection API"

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema (para PostgreSQL)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements primero (para aprovechar caché de Docker)
COPY requirements.txt .

# Instala dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia el código de la aplicación
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar la app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]