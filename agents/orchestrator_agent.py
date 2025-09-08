from typing import Dict, Type
from agents.code_review_agents import CodeReviewAgent


class OrchestratorAgent:
    def __init__(self, agents: Dict[str, Type['CodeReviewAgent']]):
        self.agents = agents

    def decide_agent(self, code_snippet: str) -> 'CodeReviewAgent':
        if "public class" in code_snippet or "import java" in code_snippet:
            return self.agents["java"]
        else:
            return self.agents["default"]

    def orchestrate_review(self, code_snippet: str, context: str = "") -> str:
        selected_agent = self.decide_agent(code_snippet)
        review_result = selected_agent.review(code_snippet, context)
        return review_result
