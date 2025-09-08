from typing import Dict, Type
from agents.code_review_agents import CodeReviewAgent
import logging

logger = logging.getLogger(__name__)

class OrchestratorAgent:
    def __init__(self, agents: Dict[str, Type['CodeReviewAgent']]):
        self.agents = agents
        logger.info("OrchestratorAgent initialized.")

    def decide_agent(self, code_snippet: str) -> 'CodeReviewAgent':
        logger.info(f"OrchestratorAgent deciding for code snippet: {code_snippet[:100]}...")
        if "public class" in code_snippet or "import java" in code_snippet:
            logger.info("Detected Java code, selecting Java agent.")
            return self.agents["java"]
        else:
            logger.info("No specific language detected, selecting default agent.")
            return self.agents["default"]
