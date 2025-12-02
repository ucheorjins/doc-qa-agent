import os
import pdfplumber
from docx import Document
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class DocumentManager:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.docs = []
        self.embeddings = None

    def load_document(self, text):
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        self.docs = chunks
        self.embeddings = self.model.encode(chunks)

    def retrieve_context(self, query, top_k=3):
        if self.embeddings is None or len(self.embeddings) == 0:
            return None
        query_vec = self.model.encode([query])
        sims = cosine_similarity(query_vec, self.embeddings)[0]
        top_indices = np.argsort(sims)[::-1][:top_k]
        context = "\n".join([self.docs[i] for i in top_indices])
        return context

    def suggest_questions(self, num_suggestions=3):
        if not self.docs:
            return []
        suggestions = [chunk[:120].strip().replace('\n', ' ') + '...' for chunk in self.docs[:num_suggestions]]
        return suggestions