from api.src.domain.ports.transaction_repository import TransactionRepository
from api.src.domain.models.transaction import Transaction
from api.src.infrastructure.adapters.mongo.config import MongoConfig

class MongoTransactionRepository(TransactionRepository):
    def __init__(self):
        self.db = MongoConfig.get_database()
        self.collection = self.db.transaction

    async def get_all(self):
        cursor = self.collection.find()
        transactions = []
        async for document in cursor:
            transaction = Transaction(
                user_id=document["user_id"],
                amount=document["amount"],
                type=document["type"],
                idempotency_key=document["id"],
                status=document.get("status", "pending")
            )
            transactions.append(transaction)
        return transactions

    async def save(self, transaction: Transaction) -> None:
        transaction_dict = {
            "id": transaction.idempotency_key,
            "user_id": transaction.user_id,
            "amount": transaction.amount,
            "type": transaction.type,
            "status": transaction.status
        }
        # Insertamos en la colección
        await self.collection.insert_one(transaction_dict)

    async def get_by_id(self, idempotency_id: str) -> Transaction:
        document = await self.collection.find_one({"id": idempotency_id})
        if document:
            return Transaction(
                user_id=document["user_id"],
                amount=document["amount"],
                type=document["type"],
                idempotency_key=document["id"],
                status=document.get("status", "pending")
            )
        return None
