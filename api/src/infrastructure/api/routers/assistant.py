from fastapi import APIRouter, HTTPException
from api.src.application.dtos.summarze import SummarizeType
from api.src.infrastructure.adapters.mongo.assistant_mongo_repository import MongoAssistantRepository
from api.src.infrastructure.adapters.llm.gemini_adapter import GeminiAPI
from api.src.domain.models.assistant import AssistantRequestResponse

router = APIRouter()

@router.post("/summarize")

async def summarize(request: SummarizeType):
    repository = MongoAssistantRepository()
    text = request.text
    # GeminiAPI es sincrono (usa requests), asi que lo dejamos asi o lo envolvemos si bloqueara mucho
    # Pero para este fix, lo importante es await repository.save
    summarize = GeminiAPI(text)
    try:
        await repository.save(AssistantRequestResponse(request=text, response=summarize))
        return {"summary": summarize, "data": request.text}
    except Exception as e:
        print(f"error assistant information: {e}")
        return {"summary": "error"}
    