# embeddings.py
"""
Builds the local Chroma vector store from data/processed/chunks.json
"""

# Import libraries
from pathlib import Path
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Constants
PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
CHUNKS_FILE = PROCESSED_DIR / "chunks.json"
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "ragnar_lore"


def load_chunks(chunks_path: Path = CHUNKS_FILE) -> list[dict]:
    """Loads the list of chunk dicts"""

    with open(chunks_path, encoding = "utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        raise ValueError(f"No chunks found in {chunks_path}. Run rag/ingestion.py first")

    return chunks


def get_embedding_function() -> HuggingFaceEmbeddings:
    """
    Loads embedding function used for both indexing chunks 
    and embedding queries at retrieval time
    """

    return HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL)


def build_vector_store(chunks: list[dict] | None = None, persist_directory: Path = CHROMA_DIR, collection_name: str = COLLECTION_NAME) -> Chroma:
    """
    Embeds every chunk and saves them into a fresh local Chroma
    collection, deleting any existing same name collection first
    """

    # Load chunk list
    if chunks is None:
        chunks = load_chunks()

    # Get id, metadata, and text from each chunk
    ids = [chunk["chunk_id"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]
    texts = [chunk["text"] for chunk in chunks]
    
    # Load the embedding function
    embedding_function = get_embedding_function()

    # Delete any existing same name collection
    Chroma(collection_name = collection_name,
           embedding_function = embedding_function,
           persist_directory = str(persist_directory)).delete_collection()

    # Create vector store
    vector_store = Chroma.from_texts(texts = texts, embedding = embedding_function,
                                     metadatas = metadatas, ids= ids,
                                     collection_name = collection_name,
                                     persist_directory = str(persist_directory))

    return vector_store


def main() -> Chroma:
    """Loads and uploads chunks into Chroma vector store"""

    chunks = load_chunks()
    vector_store = build_vector_store(chunks)

    print(f"Embedded {len(chunks)} chunks into Chroma collection {COLLECTION_NAME}' at {CHROMA_DIR}")
    return vector_store


if __name__ == "__main__":
    main()
