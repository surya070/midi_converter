from google import genai
import os

class ExplanationAgent:
    def __init__(self):
        self.client = genai.Client()
        self.model = "gemini-2.5-flash"

    def run(self):
        prompt = """
Explain the orchestration decisions in academic but simple language.
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text
