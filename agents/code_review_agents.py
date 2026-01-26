from abc import ABC, abstractmethod


class CodeReviewAgent(ABC):

    @abstractmethod
    def review(self, code_snippet: str, context: str = "") -> str:
        pass
