from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Ollama


class LLMService:
    def __init__(self, model_name="gemma:2b"):
        self.llm = Ollama(model=model_name)

        # Define a simple prompt + chain
        prompt = PromptTemplate(
            input_variables=["question"],
            template="Answer the following question clearly:\n{question}"
        )
        self.chain = LLMChain(llm=self.llm, prompt=prompt)

    def ask(self, question: str) -> str:
        """Send question to the LLM and return the answer."""
        return self.chain.run(question)