"""
Comprehensive Automated Test Suite for LexisAI RAG Pipeline
"""

import sys
import unittest
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from src.document_loader import DocumentLoader
from src.text_splitter import TextSplitter
from src.embeddings import EmbeddingModel
from src.vector_store import VectorStore
from src.llm import LegalLLM
from src.rag_pipeline import RAGPipeline
from src.utils import clear_upload_folder, clear_vector_store


class MockUploadedFile:
    def __init__(self, name: str, content: bytes):
        self.name = name
        self._content = content

    def getbuffer(self):
        return self._content


class TestLexisAIRAG(unittest.TestCase):

    def setUp(self):
        clear_upload_folder()
        clear_vector_store()
        self.sample_text = """
        EMPLOYMENT AGREEMENT
        This Agreement is made on January 15, 2024, between Acme Corp ("Company") and Jane Doe ("Employee").
        
        1. Term and Termination
        This Agreement shall commence on February 1, 2024. Either party may terminate this agreement with 30 days written notice.
        
        2. Confidentiality
        The Employee agrees not to disclose any trade secrets or proprietary information of the Company.
        
        3. Governing Law
        This Agreement shall be governed by the laws of the State of California.
        """
        self.test_file_path = root_dir / "data" / "uploads" / "sample_contract.txt"
        self.test_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.test_file_path, "w", encoding="utf-8") as f:
            f.write(self.sample_text)

    def tearDown(self):
        clear_upload_folder()
        clear_vector_store()

    def test_document_loader_txt(self):
        loader = DocumentLoader()
        text, metadata = loader.load_document(self.test_file_path)
        self.assertIn("EMPLOYMENT AGREEMENT", text)
        self.assertEqual(len(metadata), 1)

    def test_text_splitter(self):
        splitter = TextSplitter()
        pages = [{"page": 1, "text": self.sample_text}]
        chunks = splitter.split_document(pages, "sample_contract.txt")
        self.assertGreater(len(chunks), 0)
        self.assertEqual(chunks[0]["source"], "sample_contract.txt")

    def test_embeddings_and_vector_store(self):
        splitter = TextSplitter()
        pages = [{"page": 1, "text": self.sample_text}]
        chunks = splitter.split_document(pages, "sample_contract.txt")

        embedder = EmbeddingModel()
        embeddings = embedder.create_document_embeddings(chunks)
        self.assertEqual(len(embeddings), len(chunks))

        store = VectorStore()
        store.create_index(embeddings, chunks)
        self.assertEqual(store.total_chunks(), len(chunks))

        query_emb = embedder.create_query_embedding("What is the governing law?")
        results = store.search(query_emb, k=2)
        self.assertGreater(len(results), 0)
        self.assertIn("California", results[0]["text"])

    def test_rag_pipeline_end_to_end(self):
        pipeline = RAGPipeline()
        mock_file = MockUploadedFile("sample_contract.txt", self.sample_text.encode("utf-8"))
        
        total_chunks = pipeline.process_documents([mock_file])
        self.assertGreater(total_chunks, 0)
        self.assertTrue(pipeline.is_loaded())

        # Test RAG retrieval (vector store search part)
        answer, results, reasoning_details = pipeline.ask("When does the agreement commence?")
        self.assertGreater(len(results), 0)
        self.assertIsNotNone(answer)


if __name__ == "__main__":
    unittest.main()
