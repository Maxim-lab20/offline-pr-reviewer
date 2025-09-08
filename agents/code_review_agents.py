from service.llm_service import LLMService
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class CodeReviewAgent(ABC):
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        logger.info(f"{self.__class__.__name__} initialized.")

    @abstractmethod
    def review(self, code_snippet: str) -> str:
        pass
