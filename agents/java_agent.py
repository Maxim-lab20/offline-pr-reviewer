from agents.code_review_agents import CodeReviewAgent
from service.llm_service import LLMService


class JavaCodeReviewAgent(CodeReviewAgent):
    def __init__(self, llm_service: LLMService):
        super().__init__(llm_service)

    def review(self, code_snippet: str, context: str = "") -> str:
        prompt = f"""You are a Java code review agent.
        Please review the following code snippet provided between the special characters `***START_CODE***` and `***END_CODE***`. 
        Identify the language if possible. Focus on best practices, potential bugs, and areas for improvement. 
        Present your suggestions as a bulleted list:

        ***START_CODE***
        {code_snippet}
        ***END_CODE***

        Suggestions:
        """
        review_result = self.llm_service.ask(prompt, context=context)
        return review_result