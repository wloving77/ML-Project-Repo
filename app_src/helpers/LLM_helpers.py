import os
import requests
import json
from dotenv import load_dotenv
import google.generativeai as genai


class GeminiLLMHelper:
    """
    Helper class to interact with the Gemini API for LLM requests.
    """

    def __init__(self):
        # Load environment variables from .env file, you may need to modify the path depending on where your .env file is located
        # load_dotenv("../.env")
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("API credentials are not set in the .env file.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def send_request(self, prompt, context=None):
        """
        Sends a request to the LLM with a preamble, user prompt, and optional context.

        :param prompt: The user's query or input prompt.
        :param context: A list of research papers to summarize (default: None).
        :return: The response from the LLM.
        """
        if context is None:
            context = []

        # Preamble for context
        model_preamble = "You are a research assistant specializing in helping students at the University of Virginia identify and connect with professors for research opportunities. Your role is to provide concise and relevant recommendations based solely on the provided Retrieval-Augmented Generation (RAG) information. Each paper in the provided data includes a title and an associated professor. Based on this data, your task is to recommend professors that students might consider contacting, along with any relevant context from the provided papers. After recommending professors, summarize the papers associated with each professor to give the student a clearer understanding of their research areas. You must not reference information outside of the RAG-provided data. If the information appears incomplete, focus on making actionable recommendations based on the available details."

        additional_instructions = (
            "Do not write any Markdown, the frontend cannot compile it"
        )

        # Construct the final prompt
        final_prompt = (
            f"{model_preamble}\n\n"
            f"User Prompt: {prompt}\n\n"
            f"Papers to Summarize:\n{json.dumps(context, indent=4)}"
            f"\n\n{additional_instructions}"
        )

        # Call the LLM with the final prompt
        response = self.model.generate_content(final_prompt)

        final_response = response.candidates[0].content.parts[0].text

        return final_response
