import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI()

    def stream_chat(self, messages, model):
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return completion.choices[0].message.content

