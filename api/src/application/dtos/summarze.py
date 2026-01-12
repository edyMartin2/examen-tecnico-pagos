from pydantic import BaseModel

class SummarizeType(BaseModel):
    text: str