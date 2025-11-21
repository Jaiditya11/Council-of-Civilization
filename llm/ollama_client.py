import requests
import json
import logging

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434", model="mistral"):
        self.base_url = base_url
        self.model = model

    def generate(self, prompt, system_prompt=None, context=None):
        """
        Generate a response from the Ollama model.
        """
        url = f"{self.base_url}/api/generate"
        
        full_prompt = prompt
        if system_prompt:
            pass

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_ctx": 4096 
            }
        }

        if system_prompt:
            payload["system"] = system_prompt

        if context:
             payload["context"] = context

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama: {e}")
            return {"error": str(e)}

    def chat(self, messages):
        """
        Chat with the Ollama model using the /api/chat endpoint.
        messages: list of dicts [{'role': 'user', 'content': '...'}, ...]
        """
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama: {e}")
            return {"error": str(e)}
