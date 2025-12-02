import os
import sys
import pdfplumber
from docx import Document

def load_backend_doc(path, doc_manager):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        with pdfplumber.open(path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif ext in [".docx", ".doc"]:
        doc = Document(path)
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    elif ext in [".txt", ".md"]:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported document format.")

    doc_manager.load_document(text)
    print(f"Loaded and indexed backend document: {path}")
