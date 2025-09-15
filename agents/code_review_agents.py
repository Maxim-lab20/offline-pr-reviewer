from service.llm_service import LLMService
from abc import ABC, abstractmethod


class CodeReviewAgent(ABC):
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    @abstractmethod
    def review(self, code_snippet: str, context: str = "") -> str:
        pass
