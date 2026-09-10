import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
    SMTP_EMAIL = st.secrets.get("SMTP_EMAIL", os.getenv("SMTP_EMAIL"))
    SMTP_APP_PASSWORD = st.secrets.get("SMTP_APP_PASSWORD", os.getenv("SMTP_APP_PASSWORD"))
except Exception:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")

# --- Model Configuration ---
LLM_MODEL = "gemini/gemini-3.5-flash-lite"
EMBEDDING_MODEL = "models/gemini-embedding-001"
LLM_TEMPERATURE = 0.3

# --- Embedding Provider Toggle ---
USE_LOCAL_EMBEDDINGS = True
LOCAL_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# --- RAG Pipeline Configuration ---
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
RETRIEVAL_CANDIDATES = 6
FINAL_K = 2

# --- Business Rules ---
REFUND_APPROVAL_THRESHOLD = 50.0

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "database", "aura.db")
CHROMA_DIR = os.path.join(BASE_DIR, "knowledge_base", "chroma_store")
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "knowledge_base")