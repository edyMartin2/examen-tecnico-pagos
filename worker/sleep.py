import asyncio
import json
import random
import os
import sys
import aio_pika
from dotenv import load_dotenv

# Force stdout flushing
sys.stdout.reconfigure(line_buffering=True)
print("[Worker] Script iniciado (Pre-imports completados)", flush=True)

# Agregamos el directorio raíz al path
sys.path.append(os.getcwd())
print(f"[Worker] CWD: {os.getcwd()}", flush=True)
print(f"[Worker] Python Path: {sys.path}", flush=True)

try:
    from api.src.infrastructure.adapters.mongo.config import MongoConfig
    print("[Worker] Importación de MongoConfig exitosa", flush=True)
except Exception as e:
    print(f"[Worker] Error importando MongoConfig: {e}", flush=True)

load_dotenv()

RABBITMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER", "user_admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", "password_secret")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
QUEUE_NAME = "transaction_processing_queue"

async def process_transaction(message: aio_pika.IncomingMessage):
    async with message.process():
        print(f"Mensaje recibido raw: {message.body}", flush=True)
        data = json.loads(message.body)
        transaction_id = data.get("transaction_id")
        
        print(f"Procesando ID: {transaction_id}", flush=True)
        
        sleep_time = random.randint(5, 10)
        print(f"Durmiendo {sleep_time} segundos...", flush=True)
        await asyncio.sleep(sleep_time)
        
        final_status = random.choice(["success", "failed"])
        
        try:
            db = MongoConfig.get_database()
            collection = db.transaction
            
            result = await collection.update_one(
                {"id": transaction_id},
                {"$set": {"status": final_status}}
            )
            print(f"Actualizado en Mongo: {result.modified_count} documentos. Nuevo estado: {final_status}", flush=True)
        except Exception as e:
            print(f"Error actualizando Mongo: {e}", flush=True)

async def main():
    print(f"Conectando a RabbitMQ...", flush=True)
    
    connection = await aio_pika.connect_robust(
        f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
    )
    
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        
        print("Esperando mensajes...", flush=True)
        
        await queue.consume(process_transaction)
        await asyncio.Future()

if __name__ == "__main__":
    print("Entrando al main...", flush=True)
    while True:
        try:
            asyncio.run(main())
        except (ConnectionRefusedError, aio_pika.exceptions.AMQPConnectionError) as e:
            print(f"Fallo de conexión ({e}). Reintentando en 5s...", flush=True)
            import time
            time.sleep(5)
        except KeyboardInterrupt:
            print("Detenido por usuario.", flush=True)
            break
        except Exception as e:
            print(f"Error crítico: {e}", flush=True)
            import time
            time.sleep(5)
