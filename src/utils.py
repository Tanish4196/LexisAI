"""
Utility Module
Provides helper functions for directory cleanup, text sanitation, and key validation.
"""

import shutil
from pathlib import Path
from src.config import UPLOAD_FOLDER, VECTOR_STORE_PATH, FAISS_INDEX_PATH, METADATA_PATH


def clear_upload_folder():
    """Removes all files in the upload folder."""
    folder = Path(UPLOAD_FOLDER)
    if folder.exists():
        for file in folder.iterdir():
            if file.is_file():
                try:
                    file.unlink()
                except Exception as e:
                    print(f"Error deleting file {file}: {e}")


def clear_vector_store():
    """Removes saved vector store index and metadata files."""
    if Path(FAISS_INDEX_PATH).exists():
        try:
            Path(FAISS_INDEX_PATH).unlink()
        except Exception as e:
            print(f"Error deleting index: {e}")

    if Path(METADATA_PATH).exists():
        try:
            Path(METADATA_PATH).unlink()
        except Exception as e:
            print(f"Error deleting metadata: {e}")


def clean_text(text: str) -> str:
    """Cleans up text by stripping excess whitespace."""
    if not text:
        return ""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)
