import os
import ollama
from dotenv import load_dotenv
load_dotenv()


class OllamaClient:
    def __init__(self):
        self.client = ollama.Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))

    def stream_chat(self, messages, model):
        stream = self.client.chat(model=model, messages=messages)
        return stream['message']['content']