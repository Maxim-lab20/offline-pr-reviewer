import ollama


class LLMService:
    def __init__(self):
        self.model_name = "gemma:2b"

    def ask(self, prompt: str, context: str = "") -> str:
        full_prompt = f"Context: {context}\n\nQuestion: {prompt}" if context else prompt
        try:
            response = ollama.chat(model=self.model_name, messages=[{'role': 'user', 'content': full_prompt}])
            return response['message']['content']
        except Exception as e:
            print(f"Error communicating with Ollama: {e}")
            return f"Error: Could not get response from LLM. {e}"


    