from dataclasses import dataclass

@dataclass
class AssistantRequestResponse:
    request: str
    response: str