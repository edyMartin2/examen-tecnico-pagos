FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Usamos el contexto raíz para poder acceder a 'api' y 'worker'
COPY worker/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el contexto (incluyendo api/ y worker/)
COPY . .

ENV PYTHONPATH=/app
ENV MODULE_NAME="sleep"

# Ejecutamos el script del worker
CMD ["python", "worker/sleep.py"]
