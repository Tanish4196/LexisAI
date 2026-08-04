"""
Document Summarizer

Creates a structured summary of legal documents.
"""

from src.llm import LegalLLM


class DocumentSummarizer:

    def __init__(self, llm=None):
        self.llm = llm if llm else LegalLLM()

    # ------------------------------------
    # Generate Summary
    # ------------------------------------

    def summarize(self, document):
        return self.llm.summarize(document)