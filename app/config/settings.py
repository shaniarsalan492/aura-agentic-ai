import os
from dotenv import load_dotenv
import tempfile

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


def _get_writable_data_dir():
    """Returns a writable directory for the database and vector store.
    Tries the project folder first (normal local development); falls back
    to the system temp directory if the project folder is read-only
    (e.g. on Streamlit Community Cloud, where the cloned repo is not writable)."""
    candidate = os.path.join(BASE_DIR, "database")
    try:
        os.makedirs(candidate, exist_ok=True)
        test_file = os.path.join(candidate, ".write_test")
        with open(test_file, "w") as f:
            f.write("ok")
        os.remove(test_file)
        return BASE_DIR
    except (OSError, PermissionError):
        temp_dir = os.path.join(tempfile.gettempdir(), "aura_data")
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir


_DATA_DIR = _get_writable_data_dir()
DB_PATH = os.path.join(_DATA_DIR, "database", "aura.db") if _DATA_DIR == BASE_DIR else os.path.join(_DATA_DIR, "aura.db")
CHROMA_DIR = os.path.join(_DATA_DIR, "knowledge_base", "chroma_store") if _DATA_DIR == BASE_DIR else os.path.join(_DATA_DIR, "chroma_store")
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "knowledge_base")  # source .txt/.pdf files are read-only, always from repo