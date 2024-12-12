import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai


class GeminiLLMHelper:
    """
    Helper class to interact with the Gemini API for LLM requests.
    """

    def __init__(self):
        # Load environment variables from .env file, you may need to modify the path depending on where your .env file is located
        load_dotenv("../../.env)")
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("API credentials are not set in the .env file.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def send_request(self, prompt):

        response = self.model.generate_content(prompt)

        return response
