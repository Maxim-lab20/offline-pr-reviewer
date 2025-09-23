
import os
import google.generativeai as genai

class GeminiLLMService:
    def __init__(self):
        genai.configure(api_key='AIzaSyB2VFEnCaa1z5umpNTA2Q5AmwYxkwUcRlM')
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')

    def ask(self, prompt: str):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating content from Gemini: {e}"
