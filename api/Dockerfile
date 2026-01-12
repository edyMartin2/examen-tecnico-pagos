FROM python:3.10-slim

WORKDIR /app

# Usamos el contexto raíz para encontrar api/requirements.txt
COPY api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el contexto (incluyendo api/ y worker/)
COPY . .

EXPOSE 8000

ENV MODULE_NAME="main"
ENV VARIABLE_NAME="app"
ENV PYTHONPATH=/app
CMD ["uvicorn", "api.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
