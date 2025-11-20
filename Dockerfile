FROM python:3.11-slim

WORKDIR /app

# Instala las dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente
COPY . .

ENV PYTHONUNBUFFERED=1

# Usar Gunicorn SIEMPRE en Render
CMD gunicorn app:server --workers=1 --threads=4 --timeout=180 --bind 0.0.0.0:${PORT:-8050}
