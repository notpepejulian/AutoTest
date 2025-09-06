FROM python:3.11-slim

WORKDIR /app

# Crear usuario backend
RUN groupadd -r backend && useradd -r -g backend backend

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias como root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Cambiar al usuario frontend
USER backend

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la aplicación (modo producción sin --reload)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
