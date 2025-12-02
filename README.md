# Document Q&A Agent (OpenAI + Ollama + Gradio)

A lightweight document-aware chatbot that can answer questions from PDF, DOCX, or text files using:

- Sentence-Transformer embeddings\*\* for context retrieval

- LLM models (OpenAI and Ollama here) for answer generation

- A clean Gradio UI for interaction

This project demonstrates real-world LLM engineering: retrieval pipelines, dual-model support, and an interactive user interface.

Features

- Load PDFs, DOCX, or raw text files

- Automatic document chunking + embedding (MiniLM-L6-v2)

- Switch between OpenAI and Ollama models

- Real-time Q&A with context injection

- Gradio interface for easy testing

- Basic unit tests included

---

# Installation

### Clone the repo

- git clone:

```text
https://github.com/ucheorjins/doc-qa-agent.git
```

- cd doc-qa-agent

### Create and activate virtual environment

```bash
  python3 -m venv .venv
```

source:

```bash
.venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

NB:

- Install Ollama separately at

```text
  https://ollama.ai
```

- Put your OpenAI API key in a .env file.

---

### Environment Variables

Create a .env file:

```text
- OPENAI_API_KEY=your_key_here

- LLM_PROVIDER= "openai" or "ollama"

- OLLAMA_HOST=http://localhost:11434
```

---

# Running the App

- ```bash
  cd src
  ```

- ```bash
  python main.py
  ```

````

-Gradio will start and print a local URL: Running on
```text
http://127.0.0.1:7860/
````

---

# Running Tests

```text
pytest tests
```

---

# Future Improvements

- Add user file upload for QA process

- Add vector database support (FAISS / Chroma)

- Add multiple document support

- Deploy online (HuggingFace Spaces or Docker)

---

# License

MIT License. Free to use and modify.
