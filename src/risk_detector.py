"""
Risk Detection Module

Analyses legal documents for potential legal and business risks.
"""

from src.llm import LegalLLM


class RiskDetector:

    def __init__(self, llm=None):
        self.llm = llm if llm else LegalLLM()

    # ----------------------------------------
    # Detect Risks
    # ----------------------------------------

    def detect(self, document):
        return self.llm.detect_risks(document)