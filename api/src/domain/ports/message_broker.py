from abc import ABC, abstractmethod

class MessageBrokerInfo(ABC):
    @abstractmethod
    async def publish(self, queue: str, message: dict) -> None:
        """Publishes a message to a queue"""
        pass
