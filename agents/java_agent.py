from agents.code_review_agents import CodeReviewAgent
from service.llm_service import LLMService


class JavaCodeReviewAgent(CodeReviewAgent):
    def __init__(self, llm_service: LLMService):
        super().__init__(llm_service)

    def review(self, code_snippet: str, context: str = "") -> str:
        prompt = f"Review the following Java code for best practices, potential bugs, and areas for improvement:\n\n```java\n{code_snippet}\n```"
        review_result = self.llm_service.ask(prompt, context=context)
        return review_result