"""
OpenRouter LLM Module

Handles:
- Question Answering (RAG)
- Summarization
- Clause Extraction
- Risk Detection
- Contract Comparison
- Date Extraction

Uses OpenRouter API endpoint (https://openrouter.ai/api/v1/chat/completions)
Supports Reasoning Tokens & Preserves reasoning_details across turns.
"""

import json
import requests

from src.config import (
    get_openrouter_api_key,
    OPENROUTER_API_URL,
    OPENROUTER_MODEL
)
from src.prompt import (
    RAG_QA_PROMPT,
    SUMMARY_PROMPT,
    CLAUSE_DETECTION_PROMPT,
    RISK_ANALYSIS_PROMPT,
    DATE_EXTRACTION_PROMPT,
    COMPARISON_PROMPT
)


class LegalLLM:

    def __init__(self, model_name=None):
        self.model_name = model_name or OPENROUTER_MODEL

    # ---------------------------------------
    # Multi-turn OpenRouter Request with Reasoning
    # ---------------------------------------

    def generate_chat(self, messages, reasoning=True):
        """
        Sends conversation messages to OpenRouter API and returns dictionary containing:
        - content: Assistant text response
        - reasoning_details: Preserved reasoning object/details from model
        """
        api_key = get_openrouter_api_key()
        if not api_key:
            return {
                "content": "⚠️ Error: OPENROUTER_API_KEY is not configured in .env file or Streamlit secrets.",
                "reasoning_details": None
            }

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://lexisai.local",
            "X-Title": "LexisAI Legal Assistant"
        }

        # Build message history preserving reasoning_details for assistant responses
        formatted_messages = []
        for msg in messages:
            item = {
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            }
            if msg.get("role") == "assistant" and msg.get("reasoning_details"):
                item["reasoning_details"] = msg["reasoning_details"]
            formatted_messages.append(item)

        payload = {
            "model": self.model_name,
            "messages": formatted_messages
        }

        if reasoning:
            payload["reasoning"] = {"enabled": True}

        try:
            response = requests.post(
                url=OPENROUTER_API_URL,
                headers=headers,
                data=json.dumps(payload),
                timeout=90
            )

            if response.status_code != 200:
                return {
                    "content": f"⚠️ OpenRouter API Error (Status {response.status_code}): {response.text}",
                    "reasoning_details": None
                }

            res_data = response.json()
            if "choices" in res_data and len(res_data["choices"]) > 0:
                message = res_data["choices"][0]["message"]
                return {
                    "content": message.get("content") or "",
                    "reasoning_details": message.get("reasoning_details")
                }
            elif "error" in res_data:
                err_msg = res_data["error"].get("message", str(res_data["error"]))
                return {
                    "content": f"⚠️ OpenRouter API Error: {err_msg}",
                    "reasoning_details": None
                }
            else:
                return {
                    "content": f"⚠️ Unexpected response structure: {res_data}",
                    "reasoning_details": None
                }

        except Exception as e:
            return {
                "content": f"⚠️ API Connection Error: {str(e)}",
                "reasoning_details": None
            }

    # ---------------------------------------
    # Single Prompt Request
    # ---------------------------------------

    def generate(self, prompt, reasoning=True):
        res = self.generate_chat([{"role": "user", "content": prompt}], reasoning=reasoning)
        return res["content"]

    # ---------------------------------------
    # Question Answering (RAG)
    # ---------------------------------------

    def answer_question(self, context, question, chat_history=None):
        if not context or not context.strip():
            return "I couldn't find relevant information in the uploaded documents to answer your question.", None

        messages = []
        if chat_history:
            for msg in chat_history:
                item = {
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                }
                if msg.get("reasoning_details"):
                    item["reasoning_details"] = msg["reasoning_details"]
                messages.append(item)

        user_prompt = RAG_QA_PROMPT.format(context=context, question=question)
        messages.append({"role": "user", "content": user_prompt})

        res = self.generate_chat(messages, reasoning=True)
        return res["content"], res.get("reasoning_details")

    # ---------------------------------------
    # Document Summary
    # ---------------------------------------

    def summarize(self, document):
        if not document or not document.strip():
            return "⚠️ Please upload a valid document first."
        prompt = SUMMARY_PROMPT.format(document=document)
        return self.generate(prompt)

    # ---------------------------------------
    # Clause Detection
    # ---------------------------------------

    def detect_clauses(self, document):
        if not document or not document.strip():
            return "⚠️ Please upload a valid document first."
        prompt = CLAUSE_DETECTION_PROMPT.format(document=document)
        return self.generate(prompt)

    # ---------------------------------------
    # Risk Analysis
    # ---------------------------------------

    def detect_risks(self, document):
        if not document or not document.strip():
            return "⚠️ Please upload a valid document first."
        prompt = RISK_ANALYSIS_PROMPT.format(document=document)
        return self.generate(prompt)

    # ---------------------------------------
    # Date Extraction
    # ---------------------------------------

    def extract_dates(self, document):
        if not document or not document.strip():
            return "⚠️ Please upload a valid document first."
        prompt = DATE_EXTRACTION_PROMPT.format(document=document)
        return self.generate(prompt)

    # ---------------------------------------
    # Compare Contracts
    # ---------------------------------------

    def compare_documents(self, doc1, doc2):
        if not doc1 or not doc1.strip() or not doc2 or not doc2.strip():
            return "⚠️ Please upload two valid documents to compare."
        prompt = COMPARISON_PROMPT.format(doc1=doc1, doc2=doc2)
        return self.generate(prompt)