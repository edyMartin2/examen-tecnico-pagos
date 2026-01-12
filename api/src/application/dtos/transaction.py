from pydantic import BaseModel

class TransactionType(BaseModel):
    user_id: str
    amount: int
    type: str
