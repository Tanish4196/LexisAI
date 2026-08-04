"""
Date Extraction Module

Extracts all important dates and deadlines from legal documents.
"""

from src.llm import LegalLLM


class DateExtractor:

    def __init__(self, llm=None):
        self.llm = llm if llm else LegalLLM()

    # -----------------------------------------
    # Extract Dates
    # -----------------------------------------

    def extract(self, document):
        return self.llm.extract_dates(document)