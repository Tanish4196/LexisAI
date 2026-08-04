"""
Legal Prompt Templates Module
Centralizes all prompts used by the Gemini LLM for legal document analysis.
"""

RAG_QA_PROMPT = """
You are an expert Legal AI Assistant.

Answer ONLY using the supplied document context.

If the answer is not present, say:
"I couldn't find this information in the uploaded documents."

Always answer clearly and accurately based on the context.

Context:
{context}

Question:
{question}

Answer:
"""

SUMMARY_PROMPT = """
You are an experienced Legal Analyst.

Read the document carefully and generate a professional legal summary.

Return the answer in exactly this format:

# Contract Type

# Parties Involved

# Purpose

# Important Clauses

# Obligations

# Risks

# Important Dates

# Governing Law

# Overall Summary

Document:
{document}
"""

CLAUSE_DETECTION_PROMPT = """
You are an expert Legal Contract Reviewer.

Analyse the following legal document. Identify whether each clause is PRESENT or NOT FOUND.

For every clause that exists:
1. Write the clause name.
2. Explain its purpose.
3. Quote or summarize the relevant text.

Return the result using this format:

# Clause Detection Report

## Termination
Status:
Purpose:
Summary:

## Confidentiality
Status:
Purpose:
Summary:

## Payment
Status:
Purpose:
Summary:

## Intellectual Property
Status:
Purpose:
Summary:

## Indemnity
Status:
Purpose:
Summary:

## Arbitration
Status:
Purpose:
Summary:

## Governing Law
Status:
Purpose:
Summary:

## Force Majeure
Status:
Purpose:
Summary:

## Non-Compete
Status:
Purpose:
Summary:

## Renewal
Status:
Purpose:
Summary:

Document:
{document}
"""

RISK_ANALYSIS_PROMPT = """
You are an experienced Legal Risk Analyst.

Review the legal document carefully and identify every potential legal or business risk.

For each risk provide:
1. Risk Name
2. Risk Level (Low / Medium / High)
3. Explanation
4. Recommendation

Return the report using this format:

# Legal Risk Assessment

## Risk 1
Risk Name:
Risk Level:
Explanation:
Recommendation:

----------------------------------

## Risk 2
Risk Name:
Risk Level:
Explanation:
Recommendation:

----------------------------------

Also analyse these areas:
• One-sided clauses
• High penalties
• Automatic renewal
• Unlimited liability
• Missing confidentiality
• Missing termination clause
• Missing dispute resolution
• Intellectual property ownership
• Governing law concerns
• Compliance issues
• Payment risks
• Data privacy risks
• Force majeure issues
• Ambiguous wording

At the end provide:

# Overall Risk Score
Choose one: Low Risk | Medium Risk | High Risk

Document:
{document}
"""

DATE_EXTRACTION_PROMPT = """
You are an expert Legal Document Analyst.

Read the following legal document carefully and extract ALL important dates.

Return your answer in this format:

# Important Dates

## Effective Date
Value:
Description:

--------------------------------

## Contract Expiry Date
Value:
Description:

--------------------------------

## Renewal Date
Value:
Description:

--------------------------------

## Notice Period
Value:
Description:

--------------------------------

## Payment Due Dates
Value:
Description:

--------------------------------

## Compliance Deadlines
Value:
Description:

--------------------------------

## Filing Deadlines
Value:
Description:

--------------------------------

## Grace Period
Value:
Description:

--------------------------------

## Other Important Dates
List every important legal date found.

--------------------------------

# Timeline
Create a chronological timeline of all events.

Document:
{document}

If any date is not mentioned, write: Not Found.
"""

COMPARISON_PROMPT = """
You are an expert Legal Contract Analyst.

Compare the following two legal documents.

Return your analysis in the following format:

# Executive Summary
Provide a short summary of the major differences.

------------------------------------

# Clause Comparison
Compare key clauses (Parties, Purpose, Payment Terms, Confidentiality, IP, Termination, Liability, Indemnity, Force Majeure, Governing Law, Arbitration, Renewal).
For every clause mention:
- Document A
- Document B
- Difference

------------------------------------

# Added Clauses
List clauses that appear only in Document B.

------------------------------------

# Removed Clauses
List clauses that appear only in Document A.

------------------------------------

# Modified Clauses
Explain important modifications.

------------------------------------

# Legal Impact
Explain how these differences may affect the parties involved.

------------------------------------

# Recommendation
Suggest which document appears safer and why.

=========================
DOCUMENT A:
{doc1}

=========================
DOCUMENT B:
{doc2}
"""
