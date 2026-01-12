from pydantic import BaseModel

class TransactionAsyncProcessRequest(BaseModel):
    id: str
