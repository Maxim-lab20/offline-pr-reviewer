import ollama
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, model_name: str):
        self.model_name = model_name
        logger.info(f"LLMService initialized with model: {model_name}")

    def ask(self, prompt: str) -> str:
        logger.info(f"Asking LLM with prompt: {prompt[:100]}...")
        try:
            response = ollama.chat(model=self.model_name, messages=[{'role': 'user', 'content': prompt}])
            logger.info("Received response from LLM.")
            return response['message']['content']
        except Exception as e:
            logger.error(f"Error communicating with Ollama: {e}")
            print(f"Error communicating with Ollama: {e}")
            return f"Error: Could not get response from LLM. {e}"


    