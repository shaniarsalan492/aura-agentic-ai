from crewai import LLM
from app.config.settings import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE

llm = LLM(
    model=LLM_MODEL,
    api_key=GOOGLE_API_KEY,
    temperature=LLM_TEMPERATURE
)