from agents.default_agent import DefaultCodeReviewAgent
from agents.java_agent import JavaCodeReviewAgent
from agents.orchestrator_agent import OrchestratorAgent
from service.llm_service import LLMService
from service.rag_service import RAGService # Import RAGService
import os


class ReviewService:
    def __init__(self):
        self.llm_service = LLMService(model_name="gemma:2b")
        
        # Initialize RAGService
        self.rag_service = RAGService(document_paths=["RAG_CONTEXT/java_code_standards.txt", "RAG_CONTEXT/python_code_standards.txt"]) # Initialize RAGService with the new files

        # Configure agents
        self.java_agent = JavaCodeReviewAgent(self.llm_service)
        self.default_agent = DefaultCodeReviewAgent(self.llm_service)

        self.agents = {
            "java": self.java_agent,
            "default": self.default_agent
        }
        self.orchestrator = OrchestratorAgent(self.agents)

    def decide_and_review(self, code_snippet: str) -> str:
        # Retrieve context from RAG
        retrieved_context = self.rag_service.retrieve_context(code_snippet)

        # Orchestrate the review using the OrchestratorAgent
        review_result = self.orchestrator.orchestrate_review(code_snippet, retrieved_context)
        return review_result