import os
import aio_pika
import json
from api.src.domain.ports.message_broker import MessageBrokerInfo

class RabbitMQBroker(MessageBrokerInfo):
    def __init__(self):
        # En un entorno real, estos valores vendrían de variables de entorno protegidas
        self.user = os.getenv("RABBITMQ_DEFAULT_USER", "user_admin")
        self.password = os.getenv("RABBITMQ_DEFAULT_PASS", "password_secret")
        self.host = os.getenv("RABBITMQ_HOST", "rabbitmq")
        self.port = int(os.getenv("RABBITMQ_PORT", 5672))
        
    async def publish(self, queue: str, message: dict) -> None:
        connection = await aio_pika.connect_robust(
            f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"
        )

        async with connection:
            channel = await connection.channel()
            # Declaramos la cola para asegurarnos de que exista
            await channel.declare_queue(queue, durable=True)
            
            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=queue,
            )
