from dataclasses import dataclass

@dataclass
class Transaction:
    user_id: str
    amount: int
    type: str
    idempotency_key: str
    status: str = "pending"