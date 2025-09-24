from agents.code_review_agents import CodeReviewAgent
from service.gemini_llm_service import GeminiLLMService
from typing_extensions import override


class JavaCodeReviewAgent(CodeReviewAgent):
    def __init__(self):
        self.llm_service = GeminiLLMService()

    @override
    def review(self, code_snippet: str, context: str = "") -> str:
        full_prompt = f"""Context: {context}

        You are a Java code review agent.
        Please review the following code snippet provided between the special characters `***START_CODE***` and `***END_CODE***`. 
        Identify issues taking in consideration:
        1. provided context
        2. java best practices

        Come up with short and concise suggestions.

        ***START_CODE***
        {code_snippet}
        ***END_CODE***
        """
        review_result = self.llm_service.ask(full_prompt)
        return review_result