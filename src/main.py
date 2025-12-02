import os
import gradio as gr

from document_manager import DocumentManager
from provider_openai import OpenAIClient
from provider_ollama import OllamaClient
from agent import TechQnAAgent
from utils import load_backend_doc
from dotenv import load_dotenv

load_dotenv()

# Constants

DEFAULT_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

DEFAULT_SYSTEM = (
    "You are an assistant that answers questions primarily based on the provided document context. "
    "If the question can be inferred or answered loosely from the context, use reasoning to provide a best-effort answer. "
    "Answer confidently like you know what you're talking about and do not say things like "
    "'from the context of the document' or 'it seems'. "
    "If it truly cannot be answered, respond with: 'Sorry, I don't have that information.' "
    "Then suggest a few questions that can be answered from the document as bullet points."
)

# Document Manager 

doc_manager = DocumentManager()
load_backend_doc("data/bulanverse.pdf", doc_manager)

# Provider and Agent

provider = OpenAIClient() if DEFAULT_PROVIDER == "openai" else OllamaClient()
model_name_map = {
    "Shikamaru (OpenAI)": DEFAULT_OPENAI_MODEL,
    "Kiba (Ollama)": DEFAULT_OLLAMA_MODEL,
}

agent = TechQnAAgent(provider, DEFAULT_OPENAI_MODEL, document_manager=doc_manager)

# Gradio UI

with gr.Blocks() as ui:
    
    gr.HTML("""
        <style>
            body {height: 100vh !important; margin: 0;}
            .gradio-container {height: 100vh !important;}
        </style>
    """)

    gr.Markdown("# **Bulanverse Chatbot**")
    gr.Markdown("Ask questions related to the system's hidden knowledge base.")

    model_choice = gr.Dropdown(
        choices=list(model_name_map.keys()),
        value="Shikamaru (OpenAI)",
        label="Select Model",
    )

    chatbot = gr.Chatbot(
        value=[{"role": "assistant", "content": "Welcome! I'm your Bulanverse knowledge base curator. Ask me anything!"}],
        label="Chat",
    )

    msg = gr.Textbox(label="Ask a question")

    def respond(message, history, model_choice):
        # Switch model + provider
        if "Ollama" in model_choice:
            agent.provider = OllamaClient()
            agent.model = DEFAULT_OLLAMA_MODEL
        else:
            agent.provider = OpenAIClient()
            agent.model = DEFAULT_OPENAI_MODEL
        
        # Ask agent
        answer = agent.ask(message)


        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": answer})

        return history, "" 

    msg.submit(
        respond,
        inputs=[msg, chatbot, model_choice],
        outputs=[chatbot, msg]
    )

if __name__ == "__main__":
    ui.launch()
