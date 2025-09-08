from agents.code_review_agents import CodeReviewAgent
from service.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)

class JavaCodeReviewAgent(CodeReviewAgent):
    def __init__(self, llm_service: LLMService):
        super().__init__(llm_service)

    def review(self, code_snippet: str) -> str:
        logger.info(f"JavaCodeReviewAgent reviewing code snippet: {code_snippet[:100]}...")
        prompt = f"Review the following Java code for best practices, potential bugs, and areas for improvement:\n\n```java\n{code_snippet}\n```"
        review_result = self.llm_service.ask(prompt)
        logger.info("JavaCodeReviewAgent review completed.")
        return review_result