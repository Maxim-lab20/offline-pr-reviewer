from agents.orchestrator_agent import OrchestratorAgent
from service.llm_service import LLMService
from service.rag_service import RAGService # Import RAGService


class ReviewService:
    def __init__(self):
        self.llm_service = LLMService()
        self.rag_service = RAGService()
        self.orchestrator = OrchestratorAgent()

    def decide_and_review(self, code_snippet: str) -> str:
        # Retrieve context from RAG
        retrieved_context = self.rag_service.retrieve_context(code_snippet)

        # Orchestrate the review using the OrchestratorAgent
        review_result = self.orchestrator.orchestrate_review(code_snippet, retrieved_context)
        return review_result