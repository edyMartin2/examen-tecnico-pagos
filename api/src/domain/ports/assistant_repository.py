from abc import ABC, abstractmethod
from api.src.domain.models.assistant import AssistantRequestResponse

class AssistantRepository(ABC):
    @abstractmethod
    async def save(self, assistant_request_response: AssistantRequestResponse) -> None:
        """Interface to save a assistant request response"""
        pass