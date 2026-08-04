"""
Document Comparison Module

Compares two legal documents and highlights similarities, differences,
missing clauses, and legal implications.
"""

from src.llm import LegalLLM


class DocumentComparator:

    def __init__(self, llm=None):
        self.llm = llm if llm else LegalLLM()

    # -----------------------------------------
    # Compare Documents
    # -----------------------------------------

    def compare(self, document1, document2):
        return self.llm.compare_documents(document1, document2)