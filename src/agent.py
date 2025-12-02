
import os

DEFAULT_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
DEFAULT_SYSTEM = (
    "You are an assistant that answers questions primarily based on the provided document context. "
    "If the question can be inferred or answered loosely from the context, use reasoning to provide a best-effort answer."
    "answer confidently like you know what you're talking about and do not say things like 'from the context of the document' or 'it seems'"
    "If it truly cannot be answered, respond with: 'Sorry. I don't have that information.' and then suggest a few questions that can be answered from the document. Make sure the suggestions are in a bullet point and based on the actual context of the document"
) 

class TechQnAAgent:
    def __init__(self, provider, model, document_manager=None):
        self.provider = provider
        self.model = model
        self.document_manager = document_manager

    def ask(self, question):
        context = self.document_manager.retrieve_context(question) if self.document_manager else None
        if not context or len(context.strip()) == 0:
            suggestions = self.document_manager.suggest_questions() if self.document_manager else []
            suggestion_text = "\n- ".join(suggestions)
            if suggestion_text:
                return f"Sorry. I don't have that information.\nYou could ask about:\n- {suggestion_text}"
            else:
                return "Sorry. I don't have that information."

        messages = [
            {"role": "system", "content": DEFAULT_SYSTEM},
            {"role": "user", "content": f"Using this document context, answer the following question as best as possible even if the answer must be inferred or loosely reasoned.\n\nContext:\n{context}\n\nQuestion: {question}"}
        ]
        return self.provider.stream_chat(messages, self.model)