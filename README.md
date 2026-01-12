# comandos
para ejecutar el proyecto

```bash
docker-compose up --build
```

# servicios

*   **API (FastAPI)**: Puerto 8000
*   **Worker (Python)**: Proceso en segundo plano
*   **Frontend (React)**: Puerto 5173
*   **MongoDB**: Puerto 27017
*   **RabbitMQ**: Puerto 5672 (Dashboard en 15672)

## URL
*   frontend: [http://localhost:5173](http://localhost:5173)



# selenium

```bash
#crear nuevo entorno y activar entorno
python3 -m venv selenium_env
source selenium_env/bin/activate

#correr selenium
cd automation
pip install -r requirements.txt
python scrape_wiki.py
```