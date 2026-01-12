from abc import ABC, abstractmethod
from api.src.domain.models.transaction import Transaction

class TransactionRepository(ABC):
    @abstractmethod
    async def save(self, transaction: Transaction) -> None:
        """Interface to save a transaction"""
        pass

    @abstractmethod
    async def get_by_id(self, idempotency_id: str) -> Transaction:
        """Interface to get a transaction by idempotency_id"""
        pass
