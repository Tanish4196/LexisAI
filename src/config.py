import os
from pathlib import Path
from dotenv import load_dotenv

# ==========================================
# Base Directory
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# Environment Variables
# ==========================================

load_dotenv(BASE_DIR / ".env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

def get_openrouter_api_key():
    """Retrieves OpenRouter API key from env or Streamlit secrets if available."""
    key = os.getenv("OPENROUTER_API_KEY", "")
    if not key:
        try:
            import streamlit as st
            if "OPENROUTER_API_KEY" in st.secrets:
                key = st.secrets["OPENROUTER_API_KEY"]
        except Exception:
            pass
    return key

# Backward compatibility getter
def get_google_api_key():
    return get_openrouter_api_key()

# ==========================================
# Streamlit
# ==========================================

PAGE_TITLE = "LexisAI - Legal Document Analysis Assistant"
PAGE_ICON = "⚖️"
LAYOUT = "wide"

# ==========================================
# Data Directories
# ==========================================

DATA_DIR = BASE_DIR / "data"

UPLOAD_FOLDER = DATA_DIR / "uploads"
VECTOR_STORE_PATH = DATA_DIR / "vector_store"

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)

# ==========================================
# FAISS Files
# ==========================================

FAISS_INDEX_PATH = VECTOR_STORE_PATH / "faiss_index.index"
METADATA_PATH = VECTOR_STORE_PATH / "metadata.pkl"

# ==========================================
# Supported Documents
# ==========================================

SUPPORTED_FILE_TYPES = [
    "pdf",
    "docx",
    "txt"
]

# ==========================================
# Text Splitter
# ==========================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ==========================================
# Embedding Model
# ==========================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ==========================================
# OpenRouter Model Settings
# ==========================================

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3-ultra-550b-a55b:free")

LLM_MODEL = OPENROUTER_MODEL
MODEL_NAME = LLM_MODEL

# ==========================================
# Retrieval
# ==========================================

TOP_K_RESULTS = 3