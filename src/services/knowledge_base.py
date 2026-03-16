"""Knowledge base lookup service — FAISS vector store backed."""

from pathlib import Path

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

from src.core.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

_vectorstore: FAISS | None = None


def _load_vectorstore() -> FAISS:
    """Load the FAISS index from disk (lazy, cached)."""
    global _vectorstore
    if _vectorstore is None:
        index_path = Path(settings.FAISS_INDEX_PATH)
        if not index_path.exists():
            raise FileNotFoundError(
                f"FAISS index not found at {index_path}. "
                "Run: uv run python -m src.knowledge_base.build_index"
            )
        embeddings = OllamaEmbeddings(
            model=settings.OLLAMA_EMBEDDING_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
        )
        _vectorstore = FAISS.load_local(
            str(index_path), embeddings, allow_dangerous_deserialization=True
        )
        logger.info("Loaded FAISS index from %s", index_path)
    return _vectorstore


def search_kb(query: str, top_k: int = 3) -> str:
    """Semantic search over the knowledge base using FAISS.

    Returns the top_k most relevant document chunks as a formatted string.
    """
    store = _load_vectorstore()
    results = store.similarity_search(query, k=top_k)

    if not results:
        return "No relevant articles found in the knowledge base."

    parts = []
    for i, doc in enumerate(results, 1):
        source = Path(doc.metadata.get("source", "unknown")).stem
        parts.append(f"[{source}]\n{doc.page_content}")

    context = "\n\n---\n\n".join(parts)
    logger.info("KB search returned %d results (%d chars)", len(results), len(context))
    return context
