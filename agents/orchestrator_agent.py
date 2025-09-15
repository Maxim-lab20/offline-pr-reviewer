from typing import Dict, Type
from agents.code_review_agents import CodeReviewAgent
from agents.default_agent import DefaultCodeReviewAgent
from agents.java_agent import JavaCodeReviewAgent
from service.llm_service import LLMService

class OrchestratorAgent:
    def __init__(self):
        self.llm_service = LLMService()
        self.java_agent = JavaCodeReviewAgent(self.llm_service)
        self.default_agent = DefaultCodeReviewAgent(self.llm_service)

        self.agents = {
            "java": self.java_agent,
            "default": self.default_agent
        }

    def decide_agent(self, code_snippet: str) -> 'CodeReviewAgent':
        if "public class" in code_snippet or "import java" in code_snippet:
            return self.agents["java"]
        else:
            return self.agents["default"]

    def orchestrate_review(self, code_snippet: str, context: str = "") -> str:
        selected_agent = self.decide_agent(code_snippet)
        review_result = selected_agent.review(code_snippet, context)
        return review_result
