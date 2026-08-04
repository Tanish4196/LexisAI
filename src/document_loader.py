"""
Document Loader Module

Supports:
- PDF
- DOCX
- TXT

Returns extracted text and metadata.
"""

import os
from pathlib import Path

from pypdf import PdfReader
from docx import Document

from src.config import (
    UPLOAD_FOLDER,
    SUPPORTED_FILE_TYPES
)


class DocumentLoader:

    def __init__(self):
        self.upload_folder = Path(UPLOAD_FOLDER)

    # -----------------------------
    # Save Uploaded File
    # -----------------------------

    def save_uploaded_file(self, uploaded_file):

        file_path = self.upload_folder / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return file_path

    # -----------------------------
    # Read PDF
    # -----------------------------

    def read_pdf(self, file_path):

        reader = PdfReader(file_path)

        pages = []

        full_text = ""

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text() or ""

            full_text += text + "\n"

            pages.append({
                "page": page_number,
                "text": text
            })

        return full_text, pages

    # -----------------------------
    # Read DOCX
    # -----------------------------

    def read_docx(self, file_path):

        document = Document(file_path)

        paragraphs = []

        full_text = ""

        for para in document.paragraphs:

            if para.text.strip():

                full_text += para.text + "\n"

                paragraphs.append(para.text)

        metadata = [
            {
                "page": 1,
                "text": full_text
            }
        ]

        return full_text, metadata

    # -----------------------------
    # Read TXT
    # -----------------------------

    def read_txt(self, file_path):

        with open(file_path, "r", encoding="utf-8") as f:

            text = f.read()

        metadata = [
            {
                "page": 1,
                "text": text
            }
        ]

        return text, metadata

    # -----------------------------
    # Load Document
    # -----------------------------

    def load_document(self, file_path):

        extension = Path(file_path).suffix.lower().replace(".", "")

        if extension not in SUPPORTED_FILE_TYPES:

            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        if extension == "pdf":

            return self.read_pdf(file_path)

        elif extension == "docx":

            return self.read_docx(file_path)

        elif extension == "txt":

            return self.read_txt(file_path)

        raise ValueError("Unknown document format")