from agents.code_review_agents import CodeReviewAgent
from service.llm_service import LLMService


class DefaultCodeReviewAgent(CodeReviewAgent):
    def __init__(self, llm_service: LLMService):
        super().__init__(llm_service)

    def review(self, code_snippet: str, context: str = "") -> str:
        prompt = f"Review the following code for best practices, potential bugs, and areas for improvement. Identify the language if possible:\n\n```\n{code_snippet}\n```"
        review_result = self.llm_service.ask(prompt, context=context)
        return review_result