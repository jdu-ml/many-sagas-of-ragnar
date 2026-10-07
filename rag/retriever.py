# retriever.py
"""
Embeds the retrieval query and searches for relevant chunks
"""

# Import libraries
from rag.embeddings import get_embedding_function, CHROMA_DIR, COLLECTION_NAME
from langchain_chroma import Chroma

# Constants
DEFAULT_K = 3
VALID_CATEGORIES = {"saga_history", "mythology"}
_vector_store = None


def get_vector_store() -> Chroma:
    """Loads Chroma store once and then reuses it"""
    global _vector_store

    if _vector_store is None:
        _vector_store = Chroma(collection_name = COLLECTION_NAME,
                               embedding_function = get_embedding_function(),
                               persist_directory = str(CHROMA_DIR))

    return _vector_store


def retrieve(query: str, k: int = DEFAULT_K, category: str | None = None) -> list[dict]:
    """
    Embeds `query` and returns the top-k nearest chunks
    """
    if not query or not query.strip():
        raise ValueError("retrieve() requires a non-empty query")

    vector_store = get_vector_store()

    if category is not None and category not in VALID_CATEGORIES:
        raise ValueError(f"category must be one of {VALID_CATEGORIES}, got '{category}'")

    filter_dict = {"category": category} if category else None

    # Retrieve top-k nearest chunks
    results = vector_store.similarity_search_with_score(query, k = k, filter = filter_dict)

    return [{"text": doc.page_content,
             "score": score,
             "title": doc.metadata.get("title"),
             "category": doc.metadata.get("category"),
             "section_heading": doc.metadata.get("section_heading"),
             "source_url": doc.metadata.get("source_url")} 
             for doc, score in results]
