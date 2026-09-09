import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys / Credentials ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD")

# --- Model Configuration ---
LLM_MODEL = "gemini/gemini-3.5-flash-lite"
EMBEDDING_MODEL = "models/gemini-embedding-001"
LLM_TEMPERATURE = 0.3

# --- Business Rules ---
REFUND_APPROVAL_THRESHOLD = 50.0  # refunds >= this amount require human approval

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "database", "aura.db")
CHROMA_DIR = os.path.join(BASE_DIR, "knowledge_base", "chroma_store")
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "knowledge_base")