from api.src.domain.ports.assistant_repository import AssistantRepository
from api.src.domain.models.assistant import AssistantRequestResponse
from api.src.infrastructure.adapters.mongo.config import MongoConfig

class MongoAssistantRepository(AssistantRepository):
    def __init__(self):
        self.db = MongoConfig.get_database()
        self.collection = self.db.assistant

    async def save(self, assistant_request_response: AssistantRequestResponse) -> None:
        assistant_dict = {
           "request": assistant_request_response.request,
           "response": assistant_request_response.response
        }
        await self.collection.insert_one(assistant_dict)
