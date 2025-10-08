from agents.code_review_agents import CodeReviewAgent
from service.gpt_llm_service import GPTLLMService
from typing_extensions import override
from pathlib import Path


class JavaCodeReviewAgent(CodeReviewAgent):
    def __init__(self):
        self.llm_service = GPTLLMService()

    @override
    def review(self, code_snippet: str, context: str = "") -> str:
        prompt_path = Path(__file__).parent / "prompts" / "java_review_prompt.txt"
        template = prompt_path.read_text(encoding="utf-8")
        full_prompt = template.format(context=context, code_snippet=code_snippet)
        review_result = self.llm_service.ask(full_prompt)
        return review_result