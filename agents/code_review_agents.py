from service.gemini_llm_service import GeminiLLMService
from abc import ABC, abstractmethod


class CodeReviewAgent(ABC):

    @abstractmethod
    def review(self, code_snippet: str, context: str = "") -> str:
        pass
