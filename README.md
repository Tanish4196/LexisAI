# ⚖️ LexisAI — Legal Document Analysis Assistant

An AI-powered assistant for analyzing legal documents using Retrieval-Augmented Generation (RAG). LexisAI lets users upload legal documents (PDF, DOCX, TXT), index their content in a FAISS vector store, and interact with the documents via a chat-style interface powered by embeddings and a large language model (Gemini or another configured model).

Key goals:
- Make legal documents searchable with semantic search.
- Provide accurate, source-cited answers to user questions using RAG.
- Offer legal-focused utilities such as clause detection, risk analysis, and contract comparison.

Live demo
- Streamlit (hosted): https://lexisai-tanishsharmaurl.streamlit.app/  
(If the app is private or uses secrets, make sure the Streamlit deployment is configured with the proper environment variables.)

---

## Table of contents

- Features
- Quick start
- Installation
- Configuration
- Run (local & Docker)
- Project structure
- Design / Workflow
- Future improvements
- Contributing
- License
- Author

---

## Features

Document handling
- Upload: PDF, DOCX, TXT
- Multiple document support
- Text extraction and optional OCR (future)

AI capabilities
- RAG-based question answering with source citation
- Chat-style conversational interface
- Document summarization
- Clause detection and extraction
- Risk and date extraction
- Contract comparison

Retrieval & storage
- SentenceTransformers embeddings
- FAISS vector store for fast similarity search
- Text chunking (configurable split size/overlap)

Tech & UI
- Streamlit frontend (Chat-style dashboard)
- Python backend
- Modular pipeline for loading, embedding, indexing, retrieving, and answering

---

## Quick start (local)

1. Clone the repository

```bash
git clone https://github.com/Tanish4196/LexisAI.git
cd LexisAI
```

2. Create and activate a virtual environment

Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Copy the example env and edit it

```bash
cp .env.example .env    # macOS / Linux
copy .env.example .env  # Windows (cmd)
```

5. Run the app

```bash
streamlit run app.py
```

Open the Streamlit URL printed in the terminal (usually http://localhost:8501).

---

## Configuration / Environment variables

The project can be configured via a `.env` file. Example variables used by the project:

```env
# Which LLM provider/model you want to use. Examples: gemini or an OpenRouter-backed model
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here

# If you use OpenRouter or another proxy, keep these
OPENROUTER_API_KEY=
OPENROUTER_MODEL=

# FAISS and storage paths
DATA_DIR=./data
UPLOADS_DIR=./data/uploads
VECTOR_STORE_DIR=./data/vector_store

# Other options
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
```

Notes:
- If the repo uses Google Gemini, set GEMINI_API_KEY or the service account credentials required by your integration.
- If you use OpenRouter (or another relay), provide OPENROUTER_API_KEY and model ID.

---

## Docker (optional)

A Dockerfile is included. Build and run with:

```bash
docker build -t lexisai:latest .
docker run --env-file .env -p 8501:8501 lexisai:latest
```

---

## Project structure

Top-level layout (shortened):

LexisAI/

```
app.py
requirements.txt
README.md
Dockerfile
.env.example

src/
├── config.py            # configuration and env handling
├── document_loader.py   # load PDFs/DOCX/TXT
├── text_splitter.py     # chunking logic
├── embeddings.py        # embed text with SentenceTransformers
├── vector_store.py      # FAISS wrapper
├── llm.py               # LLM (Gemini/OpenRouter) interface
├── rag_pipeline.py      # retrieval + generation pipeline
├── chat_manager.py      # chat history and session handling
├── summarizer.py
├── clause_detector.py
├── risk_detector.py
├── comparison.py
├── date_extractor.py
└── utils.py

data/
├── uploads/
└── vector_store/

assets/
```

(See source files in `src/` for implementation details.)

---

## Design / Workflow

1. User uploads documents via the Streamlit UI
2. Text is extracted and normalized
3. Text is chunked into overlapping passages
4. Embeddings are computed using SentenceTransformers
5. Vectors are stored in FAISS
6. On user question, top-k relevant chunks are retrieved
7. A prompt combining retrieved chunks is sent to the LLM (Gemini or configured model)
8. LLM returns an answer, including citations to source chunks

---

## Development notes

- Store vector DB files under `data/vector_store/` (not checked into Git). Add this path to `.gitignore`.
- Tune CHUNK_SIZE and CHUNK_OVERLAP in `src/text_splitter.py` to balance retrieval precision and latency.
- Use a compact SentenceTransformer model for local development to reduce memory.

---

## Future improvements

- OCR support for scanned PDFs (Tesseract or cloud OCR)
- Multi-language support and locale-aware date extraction
- Persistent cloud vector store option (e.g., Pinecone, Milvus, or cloud-hosted FAISS)
- Authentication and user accounts
- Exportable reports and PDFs
- Improved citation highlighting in the UI

---

## Contributing

Contributions are welcome. Please open issues or pull requests. Typical contribution workflow:

1. Fork the repository
2. Create a feature branch
3. Add tests and update documentation
4. Open a pull request describing the change

---

## License

This project is provided under the MIT License. See `LICENSE` for details (or add one if missing).

---

## Author

Tanish Sharma

B.Tech — Computer Science Engineering

AI • Machine Learning • Data Science
