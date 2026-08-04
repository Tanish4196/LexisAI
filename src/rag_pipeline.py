"""
RAG Pipeline

Handles:
1. Document Processing
2. Chunking
3. Embeddings
4. FAISS Index
5. Retrieval
6. OpenRouter LLM Response with Reasoning Support
"""

from src.document_loader import DocumentLoader
from src.text_splitter import TextSplitter
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore
from src.llm import LegalLLM

from src.config import TOP_K_RESULTS


class RAGPipeline:

    def __init__(self):
        self.loader = DocumentLoader()
        self.splitter = TextSplitter()
        self.embedder = EmbeddingModel()
        self.vector_store = VectorStore()
        self.llm = LegalLLM()
        self.document_text = ""

    # ------------------------------------
    # Check if loaded
    # ------------------------------------

    def is_loaded(self):
        return bool(self.document_text and self.document_text.strip())

    # ------------------------------------
    # Process Uploaded Files
    # ------------------------------------

    def process_documents(self, uploaded_files):
        all_chunks = []
        self.document_text = ""

        for uploaded_file in uploaded_files:
            file_path = self.loader.save_uploaded_file(uploaded_file)
            text, pages = self.loader.load_document(file_path)

            self.document_text += f"=== File: {uploaded_file.name} ===\n" + text + "\n\n"

            chunks = self.splitter.split_document(
                pages,
                uploaded_file.name
            )
            all_chunks.extend(chunks)

        if not all_chunks:
            self.vector_store.clear()
            return 0

        embeddings = self.embedder.create_document_embeddings(all_chunks)
        self.vector_store.create_index(embeddings, all_chunks)
        self.vector_store.save()

        return len(all_chunks)

    # ------------------------------------
    # Ask Question
    # ------------------------------------

    def ask(self, question, chat_history=None):
        if not question or not question.strip():
            return "Please provide a valid question.", [], None

        if self.vector_store.total_chunks() == 0:
            self.vector_store.load()

        if self.vector_store.total_chunks() == 0:
            return "No document context is currently loaded. Please upload documents first.", [], None

        query_embedding = self.embedder.create_query_embedding(question)
        results = self.vector_store.search(
            query_embedding,
            k=TOP_K_RESULTS
        )

        context = "\n\n".join(
            chunk["text"]
            for chunk in results
        )

        answer, reasoning_details = self.llm.answer_question(
            context,
            question,
            chat_history=chat_history
        )

        return answer, results, reasoning_details

    # ------------------------------------
    # Summary
    # ------------------------------------

    def summarize(self, text=None):
        doc = text if text is not None else self.document_text
        return self.llm.summarize(doc)

    # ------------------------------------
    # Clause Detection
    # ------------------------------------

    def detect_clauses(self, text=None):
        doc = text if text is not None else self.document_text
        return self.llm.detect_clauses(doc)

    # ------------------------------------
    # Risk Analysis
    # ------------------------------------

    def detect_risks(self, text=None):
        doc = text if text is not None else self.document_text
        return self.llm.detect_risks(doc)

    # ------------------------------------
    # Date Extraction
    # ------------------------------------

    def extract_dates(self, text=None):
        doc = text if text is not None else self.document_text
        return self.llm.extract_dates(doc)

    # ------------------------------------
    # Compare Documents
    # ------------------------------------

    def compare_documents(self, doc1, doc2):
        return self.llm.compare_documents(doc1, doc2)

    # ------------------------------------
    # Reset Pipeline
    # ------------------------------------

    def clear(self):
        self.document_text = ""
        self.vector_store.clear()