import logging

from agents.default_agent import DefaultCodeReviewAgent
from agents.java_agent import JavaCodeReviewAgent
from agents.orchestrator_agent import OrchestratorAgent
from service.llm_service import LLMService

logger = logging.getLogger(__name__)

class ReviewService:
    def __init__(self):
        logger.info("Initializing ReviewService...")
        self.llm_service = LLMService(model_name="gemma:2b")
        self.java_agent = JavaCodeReviewAgent(self.llm_service)
        self.default_agent = DefaultCodeReviewAgent(self.llm_service)

        self.agents = {
            "java": self.java_agent,
            "default": self.default_agent
        }
        self.orchestrator = OrchestratorAgent(self.agents)
        logger.info("ReviewService initialized.")

    def decide_and_review(self, code_snippet: str) -> str:
        logger.info(f"Deciding agent for code snippet: {code_snippet[:100]}...")
        selected_agent = self.orchestrator.decide_agent(code_snippet)
        logger.info(f"Selected agent: {selected_agent.__class__.__name__}")
        review_result = selected_agent.review(code_snippet)
        logger.info("Code review completed.")
        return review_result