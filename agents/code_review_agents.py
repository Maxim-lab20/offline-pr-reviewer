from service.offline_llm_service import OfflineLLMService
from abc import ABC, abstractmethod


class CodeReviewAgent(ABC):
    def __init__(self, llm_service: OfflineLLMService):
        self.llm_service = llm_service

    @abstractmethod
    def review(self, code_snippet: str, context: str = "") -> str:
        pass
