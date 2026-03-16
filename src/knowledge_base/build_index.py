"""Build the FAISS index from knowledge base documents.

Run this script to (re)build the vector store:
    uv run python -m src.knowledge_base.build_index
"""

from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

from src.core.config import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

DOCS_DIR = Path(__file__).resolve().parent / "documents"
INDEX_DIR = Path(settings.FAISS_INDEX_PATH)


def build_index() -> None:
    """Load documents, chunk them, embed, and save a FAISS index."""
    logger.info("Loading documents from %s", DOCS_DIR)
    loader = DirectoryLoader(
        str(DOCS_DIR),
        glob="**/*.md",
        loader_cls=TextLoader,
    )
    documents = loader.load()
    logger.info("Loaded %d documents", len(documents))

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(documents)
    logger.info("Split into %d chunks", len(chunks))

    # Create embeddings and build FAISS index
    embeddings = OllamaEmbeddings(
        model=settings.OLLAMA_EMBEDDING_MODEL,
        base_url=settings.OLLAMA_BASE_URL,
    )

    logger.info("Building FAISS index (this may take a moment)...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Save to disk
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(INDEX_DIR))
    logger.info("FAISS index saved to %s", INDEX_DIR)


if __name__ == "__main__":
    build_index()
