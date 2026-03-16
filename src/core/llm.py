from langchain_ollama import ChatOllama
from src.core.config import settings


def get_llm() -> ChatOllama:
    """Return a configured ChatOllama instance."""
    return ChatOllama(
        model=settings.OLLAMA_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0.3,
    )
