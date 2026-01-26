from agents.code_review_agents import CodeReviewAgent
from service.llm.gpt_llm_service import GPTLLMService
from typing_extensions import override


class DefaultCodeReviewAgent(CodeReviewAgent):
    def __init__(self):
        self.llm_service = GPTLLMService()

    @override
    def review(self, code_snippet: str, context: str = "") -> str:
        full_prompt = f"""Context: {context}

        You are a default code review agent.
        Please review the following code snippet provided between the special characters `***START_CODE***` and `***END_CODE***`. 
        Identify the language if possible. Focus on best practices, potential bugs, and areas for improvement. 
        Present your suggestions as a bulleted list:

        ***START_CODE***
        {code_snippet}
        ***END_CODE***
        """
        review_result = self.llm_service.ask(full_prompt)
        return review_result
