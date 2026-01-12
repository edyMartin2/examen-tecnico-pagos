import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

class MongoConfig:
    _client: AsyncIOMotorClient = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            # Obtenemos la URL de las variables de entorno definidas en docker-compose
            mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
            cls._client = AsyncIOMotorClient(mongo_url)
        return cls._client

    @classmethod
    def get_database(cls):
        client = cls.get_client()
        # Nombre de la base de datos definido en docker-compose
        db_name = os.getenv("DB_NAME", "transactions_db")
        return client[db_name]
