from google import genai
import os

class OrchestrationPlannerAgent:
    def __init__(self):
        self.client = genai.Client()
        self.model = "gemini-2.5-flash"  # this WILL work here

    def run(self):
        prompt = """
You are an orchestration expert.
Assign orchestral instruments to melody, harmony, and bass.
Use Violin, Viola, Cello, Bass, Flute, French Horn, Percussion.
Return STRICT JSON only.
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text
