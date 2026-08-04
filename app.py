import streamlit as st
from src.config import (
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    get_openrouter_api_key,
    OPENROUTER_MODEL
)

from src.rag_pipeline import RAGPipeline
from src.chat_manager import ChatManager
from src.utils import clear_upload_folder, clear_vector_store

# ----------------------------------------------------
# Streamlit Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)

# ----------------------------------------------------
# Session State Initialization
# ----------------------------------------------------

if "pipeline" not in st.session_state:
    st.session_state.pipeline = RAGPipeline()

if "chat" not in st.session_state:
    st.session_state.chat = ChatManager()

if "file_signatures" not in st.session_state:
    st.session_state.file_signatures = []

if "last_summary" not in st.session_state:
    st.session_state.last_summary = None

if "last_clauses" not in st.session_state:
    st.session_state.last_clauses = None

if "last_risks" not in st.session_state:
    st.session_state.last_risks = None

if "last_dates" not in st.session_state:
    st.session_state.last_dates = None

if "last_comparison" not in st.session_state:
    st.session_state.last_comparison = None

pipeline: RAGPipeline = st.session_state.pipeline
chat: ChatManager = st.session_state.chat

# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

st.sidebar.title("⚖️ LexisAI")
st.sidebar.caption(f"OpenRouter Model: `{OPENROUTER_MODEL}`")

# Check API Key Status
api_key = get_openrouter_api_key()
if not api_key:
    st.sidebar.error("⚠️ OPENROUTER_API_KEY missing from .env or Secrets!")

uploaded_files = st.sidebar.file_uploader(
    "Upload Legal Documents",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

st.sidebar.divider()

analysis_option = st.sidebar.selectbox(
    "Choose Analysis",
    [
        "Question Answering",
        "Summary",
        "Clause Detection",
        "Risk Analysis",
        "Date Extraction",
        "Compare Documents"
    ]
)

st.sidebar.divider()

if st.sidebar.button("🗑 Clear Chat & Reset Session"):
    chat.clear_chat()
    pipeline.clear()
    clear_upload_folder()
    clear_vector_store()
    st.session_state.file_signatures = []
    st.session_state.last_summary = None
    st.session_state.last_clauses = None
    st.session_state.last_risks = None
    st.session_state.last_dates = None
    st.session_state.last_comparison = None
    st.success("Session and vector store reset successfully.")
    st.rerun()

# ----------------------------------------------------
# Main Header
# ----------------------------------------------------

st.title("⚖️ LexisAI — Legal Document Analysis Assistant")

st.markdown(
    """
    Upload contracts, policies, agreements, or legal documents in the sidebar.
    Then ask questions or perform AI-powered legal analysis.
    """
)

# ----------------------------------------------------
# Process Uploaded Files Persistently
# ----------------------------------------------------

current_signatures = [(f.name, f.size) for f in uploaded_files] if uploaded_files else []

if current_signatures != st.session_state.file_signatures:
    if uploaded_files:
        with st.spinner("Processing legal documents into vector store..."):
            total_chunks = pipeline.process_documents(uploaded_files)
            st.session_state.file_signatures = current_signatures
            st.session_state.last_summary = None
            st.session_state.last_clauses = None
            st.session_state.last_risks = None
            st.session_state.last_dates = None
            st.session_state.last_comparison = None
            st.success(f"Successfully processed {len(uploaded_files)} document(s) into {total_chunks} vector chunks!")
    else:
        pipeline.clear()
        st.session_state.file_signatures = []

# Status Indicator
if pipeline.is_loaded():
    st.info(f"📄 Active Context Loaded ({pipeline.vector_store.total_chunks()} index chunks available)")
else:
    st.warning("👈 Please upload legal documents in the sidebar to begin analysis.")

st.divider()

# ----------------------------------------------------
# Question Answering (RAG)
# ----------------------------------------------------

if analysis_option == "Question Answering":

    chat.display_chat()

    question = st.chat_input("Ask anything about your uploaded legal documents...")

    if question:
        if not pipeline.is_loaded():
            st.warning("Please upload legal documents before asking questions.")
        else:
            chat_history = st.session_state.messages.copy()
            chat.add_user_message(question)

            with st.spinner("Searching document context and generating answer with OpenRouter reasoning..."):
                answer, sources, reasoning_details = pipeline.ask(question, chat_history=chat_history)

            # Store answer along with retrieved sources and reasoning details in message history
            chat.add_ai_message(answer, reasoning_details=reasoning_details, sources=sources)

            st.rerun()

    # Display sources for the latest message if present
    if st.session_state.messages:
        last_msg = st.session_state.messages[-1]
        if last_msg.get("role") == "assistant" and last_msg.get("sources"):
            st.divider()
            st.subheader("📚 Retrieved Sources for Latest Answer")
            for idx, source in enumerate(last_msg["sources"], start=1):
                with st.expander(f"Source {idx}: {source.get('source', 'Document')} | Page {source.get('page', 1)} (Relevance Score: {source.get('score', 0):.4f})"):
                    st.write(source.get("text", ""))

# ----------------------------------------------------
# Summary
# ----------------------------------------------------

elif analysis_option == "Summary":

    if not pipeline.is_loaded():
        st.warning("Please upload legal documents to generate a summary.")
    else:
        if st.button("Generate Summary") or st.session_state.last_summary:
            if not st.session_state.last_summary:
                with st.spinner("Generating legal document summary..."):
                    st.session_state.last_summary = pipeline.summarize()
            st.markdown(st.session_state.last_summary)

# ----------------------------------------------------
# Clause Detection
# ----------------------------------------------------

elif analysis_option == "Clause Detection":

    if not pipeline.is_loaded():
        st.warning("Please upload legal documents to detect clauses.")
    else:
        if st.button("Detect Clauses") or st.session_state.last_clauses:
            if not st.session_state.last_clauses:
                with st.spinner("Analysing legal clauses..."):
                    st.session_state.last_clauses = pipeline.detect_clauses()
            st.markdown(st.session_state.last_clauses)

# ----------------------------------------------------
# Risk Analysis
# ----------------------------------------------------

elif analysis_option == "Risk Analysis":

    if not pipeline.is_loaded():
        st.warning("Please upload legal documents to perform risk assessment.")
    else:
        if st.button("Analyse Risks") or st.session_state.last_risks:
            if not st.session_state.last_risks:
                with st.spinner("Evaluating legal & business risks..."):
                    st.session_state.last_risks = pipeline.detect_risks()
            st.markdown(st.session_state.last_risks)

# ----------------------------------------------------
# Date Extraction
# ----------------------------------------------------

elif analysis_option == "Date Extraction":

    if not pipeline.is_loaded():
        st.warning("Please upload legal documents to extract key dates.")
    else:
        if st.button("Extract Dates") or st.session_state.last_dates:
            if not st.session_state.last_dates:
                with st.spinner("Extracting contract dates and deadlines..."):
                    st.session_state.last_dates = pipeline.extract_dates()
            st.markdown(st.session_state.last_dates)

# ----------------------------------------------------
# Compare Documents
# ----------------------------------------------------

elif analysis_option == "Compare Documents":

    if len(uploaded_files) < 2:
        st.warning("Please upload at least two documents in the sidebar to compare them.")
    else:
        if st.button("Compare Uploaded Documents") or st.session_state.last_comparison:
            if not st.session_state.last_comparison:
                with st.spinner("Comparing uploaded documents..."):
                    file1 = pipeline.loader.save_uploaded_file(uploaded_files[0])
                    file2 = pipeline.loader.save_uploaded_file(uploaded_files[1])
                    doc1, _ = pipeline.loader.load_document(file1)
                    doc2, _ = pipeline.loader.load_document(file2)
                    st.session_state.last_comparison = pipeline.compare_documents(doc1, doc2)
            st.markdown(st.session_state.last_comparison)

# ----------------------------------------------------
# Download Chat
# ----------------------------------------------------

if st.session_state.messages:
    st.sidebar.divider()
    chat_text = chat.export_chat()
    st.sidebar.download_button(
        "📥 Download Chat Log",
        chat_text,
        file_name="legal_chat.txt"
    )